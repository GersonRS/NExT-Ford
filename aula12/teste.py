import cryptocode

str_encoded = cryptocode.encrypt("gerson","flask")
print(str_encoded)
str_decoded = cryptocode.decrypt(str_encoded, "outra coisa")
print(str_decoded)