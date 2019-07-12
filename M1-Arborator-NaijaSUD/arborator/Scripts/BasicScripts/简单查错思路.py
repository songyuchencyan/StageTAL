c=[['Iphone', 5800,"a"], ['Mac Pro', "12000","b"], ['Bike', 800,"c"]]
a=["Bike",800,"a"]
m=[x for [x,y,z] in c]
n=[[x,y] for [x,y,z] in c]
print(n)

if a[0] in m:
    print("ok")
    if [a[0],a[1]] in n:
        print("okk")
        if [a[0],a[1],a[2]] in c:
            print(ok)
        else:
            for l in c:
                if l[0]==a[0] and l[1]==a[1]:
                    a[2]=l[2]
                    print(a)
        
    else:
        print("noo")

else:
    print("no")


