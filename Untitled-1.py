s_new = f'S150 A142 B421 C532 D90\n'
angle_ik = s_new
a = angle_ik.split()
normal_ik = str()
for i in a[2:-1]:
    normal_ik += f"{str(i)} "
for i in normal_ik.split():
    print(i[1:])