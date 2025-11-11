from common.insertdanhmuc import insert_danh_muc

while True:
    tendv=input("nhap vao ten danh muc moi :")

    insert_danh_muc(tendv)
    con=input( "tiep tục thì ấn y, thoát thì ấn ký tự bất kỳ")

    if con!="y":
        break

