import io
import unittest

import avro.io
import avro.schema
from avro.datafile import MAGIC
from avro.schemanormalization import Fingerprint, ToParsingCanonicalForm


class MyTestCase(unittest.TestCase):
    def test_from_java_file(self):
        schema_map = None
        schema_fingerprint = None
        with open("exmaple.avsc", "r", encoding="utf-8") as f:
            schemas = avro.schema.parse(f.read())
            schema_map = {schema.name: schema for schema in schemas.schemas}
            schema_fingerprint = {schema.name: Fingerprint(ToParsingCanonicalForm(schema), "CRC-64-AVRO") for schema in
                                  schemas.schemas}

        with open("a.bin", "rb") as f:
            schema = schema_map["Address"]
            print(str(schema))
            fingerprint = schema_fingerprint["Address"]
            raw_bytes = f.read()
            print(raw_bytes)
            print(MAGIC)
            print(fingerprint)
            bytes_reader = io.BytesIO(raw_bytes[10:])
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(schema)
            user1 = reader.read(decoder)
            print(user1)

    def test_directly(self):
        schema_map = None
        with open("exmaple.avsc", "r", encoding="utf-8") as f:
            schemas = avro.schema.Parse(f.read())
            schema_map = {schema.name: schema for schema in schemas.schemas}

        schema = schema_map["Address"]
        writer = avro.io.DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write({"name": "Abc"}, encoder)
        raw_bytes = bytes_writer.getvalue()
        print(raw_bytes)
        bytes_reader = io.BytesIO(raw_bytes)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(schema)
        user1 = reader.read(decoder)
        print(user1)


if __name__ == '__main__':
    unittest.main()
