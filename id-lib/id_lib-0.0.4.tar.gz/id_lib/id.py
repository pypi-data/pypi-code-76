# Copyright (c) 2021 Denys Makogon. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import secrets
import time
import uuid


class ObjectID(object):
    def __get_bytes_from_object(self, uint64_value: int) -> bytes:
        a = (uint64_value >> 40).to_bytes(1, byteorder="big", signed=False)[0]
        b = (uint64_value >> 32).to_bytes(2, byteorder="big", signed=False)[-1]
        c = (uint64_value >> 24).to_bytes(3, byteorder="big", signed=False)[-1]
        d = (uint64_value >> 16).to_bytes(4, byteorder="big", signed=False)[-1]
        e = (uint64_value >> 8).to_bytes(5, byteorder="big", signed=False)[-1]
        f = uint64_value.to_bytes(6, byteorder="big", signed=False)[-1]

        return bytes((a, b, c, d, e, f))

    # 48 bits UNIX time
    def __get_epoch_bytes(self) -> bytes:
        return self.__get_bytes_from_object(int(time.time() * 1000))

    # 48 bits machineID
    def __get_machine_id_bytes(self) -> bytes:
        return self.__get_bytes_from_object(uuid.getnode())

    # 32 bits incremented secret
    def __get_bytes_from_secret(self) -> bytes:
        seeded_secret = (
            int.from_bytes(secrets.token_bytes(4), byteorder="big", signed=False) + 1
        )
        a = (seeded_secret >> 24).to_bytes(1, byteorder="big", signed=False)[0]
        b = (seeded_secret >> 16).to_bytes(2, byteorder="big", signed=False)[-1]
        c = (seeded_secret >> 8).to_bytes(3, byteorder="big", signed=False)[-1]
        d = seeded_secret.to_bytes(4, byteorder="big", signed=False)[-1]

        return bytes((a, b, c, d))

    # binary format: [ [ 48 bits time ] [ 48 bits machineID ] [ 32 bits random ] ]
    def get(self) -> str:
        return (
            (
                self.__get_epoch_bytes()
                + self.__get_machine_id_bytes()
                + self.__get_bytes_from_secret()
            )
            .hex()
            .upper()
        )


__all__ = ["ObjectID"]
