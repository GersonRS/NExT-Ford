import cryptocode

str_encoded = cryptocode.encrypt("gerson","flask")
print(str_encoded)
str_decoded = cryptocode.decrypt(str_encoded, "flask")
print(str_decoded)