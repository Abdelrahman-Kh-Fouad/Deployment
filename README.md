## Documentation 
Small documentation maded by postman [here!](documentation)

## Toml and label files 
All files the basic model app and seceondry models apps automated and changed by basic templates and rendered by jinja.

### Toml rules :

```toml
[Basic]
ip = '0.0.0.0'
model = '1eR8_1X5erBkVlliRDGa_q-0SCmegwTxc'
label = 'basic.txt'
shape = 23
[Second]
    [Second.0]
    ip = 'localhost'
    model = '1TDOD0169iEs-nvpNce00qOpleiUzUB-n'
    label = 's_0.txt'
    shape = 8
```
As you see one section for Basic file and section for secondery files.<br>
`ip` = __ip of server of section__<br>
`model` =  __file name in google drive__<br>
`label` = __labeling of model you should put it in Labels dir__<br> 
```text
Atopic
0
DermatitisLids
1
Eczema Areolae
2
```
format as you see to make it easy in parsing 
`shape` = __shape of labels in models__
