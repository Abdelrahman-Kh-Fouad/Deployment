import toml
#print (toml.load("configuration.toml"))
f = toml.load('configuration.toml')
for i in f:
    print (i)
    if type(f[i])==dict:
        for j in f[i] :
            print(j)