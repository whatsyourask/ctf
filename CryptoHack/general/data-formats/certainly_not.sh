#!/bin/bash

der_file=$1
openssl x509 -in $der_file -inform der -noout -text
