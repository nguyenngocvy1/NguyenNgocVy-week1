# Nguyễn Ngọc Vỹ
# **WEEK 1: Xử lý ảnh dùng OpenCV và Python**
# Mục lục:
1. Nhiệm vụ:
    1. Đối tượng.
    2. Yêu cầu.
    3. Công cụ/ Từ khóa.
    4. Các sản phẩm càn hoàn thành.
2. Các bước tiếp cận:
    1. Sơ đồ.
    2. Chú thích.
3. Task 1:
    1. Import thư viện.
    2. Đọc file ảnh.
    3. Tiền xử lý ảnh.
    4. Xác định viền của hạt nước
    5. Tìm viền của hạt nước để tính toán
    6. Số lượng hạt nước tìm được (tương đối)
    7. Kiểm nghiệm độ chính xác của số liệu:
4. Task 2:
    1. Reset lại img_draw để vẽ cho Task 2.
    2. Khoanh vùng đối tượng (ROI).
    3. Xác định viền, tìm viền, số lượng hạt đếm được.
    4. Đổi đơn vị.
    5. Tìm đường kính hạt.
    6. Xác định kích thước lớn nhất của hạt.
    7. Xác định phân bố hạt theo đường kính.
    8. Vẽ biểu đồ phân bố.
    9. Kiểm nghiệm tính chính xác của số liệu.
5. Tài liệu tham khảo:
# Nội dung:
## **I. Nhiệm vụ:**
1. Đối tượng:
    - Ảnh chụp hạt nước có tương phản cao đã được tiền xử lý.
    <div align='center'>
    <img src="img\week1.png" width='90%'>
    </div>
2. Yêu cầu:
    - Tìm ra được số lượng hạt trong ảnh.
    - Tìm ra phân bố hạt trong ảnh với tỉ lệ 10 micron = 1pixel
3. Công cụ/ Từ khóa:
    - Opencv 4.1 trên Jetson Nano.
    - Python (run using cmd on Jetson Nano).
    - Visual Code (text editor).
    - Image contour.
    - Edge detect opencv.
    - How to..... in python. (google search)
4. Các sản phẩm cần hoàn thành:
    - 1x báo cáo hướng tiếp cận vấn đề.
    - 1x ảnh kết quả (ảnh đã xử lý để tìm ra số hạt và phân bố hạt).
    - 1x kết quả báo cáo 2 nội dung bên trên.
    - 1x program ở dạng xxxx.py
## **II. Các bước tiếp cận:**
1. Sơ đồ.
    <div align='center'>
    <img src="img\step.png" width='90%'>
    </div>
2. Chú thích:
    - Task 1: (Object => Canny Edge detection => ...)
        - Mỗi vật thể sẽ có một đường viền xung quanh.
        - Ta sẽ đếm số hạt bằng cách đếm số viền hạt nước.
        - **nhược điểm:** vẫn chưa phân biệt được nhiều hạt nằm chồng chéo lên nhau.
    - Task 2: (Object => ROI => ...)
        - Phân bố hạt: phân bố số lượng theo kích thước.
        - Kích thước hạt ở đây chọn là đường kính hạt.
        - Đường kính hạt xấp xỉ bằng chiều rộng đường bao hình chữ nhật quanh hạt.
        - Chia số hạt trên thành các nhóm dựa vào đường kính: từ 0 đến dưới 10 , 10 đến dưới 20,... đến hết đường kính lớn nhất.
        - Đếm số hạt trong mỗi khoảng đường kính.
## **III. Task 1: Tìm số lượng hạt trong ảnh**
1. Import thư viện:
    ```python
    import cv2
    import numpy as np #drawBoundingRect
    import math #roundUp
    import matplotlib.pyplot as plt #draw Diagram
    ```
2. Đọc file ảnh:
    - Sử dụng hàm cv2.imread() trong OpenCV để input file ảnh:
    - Cú pháp:
    ```python
    cv2.imread("path_filename",flag)
    ```
    - flag
        - flag = 1: input ảnh màu không có độ trong suốt (bỏ qua kênh Alpha - kênh trong suốt hình ảnh).
        - flag = 2: input ảnh trắng đen.
        -	flag = -1: input ảnh màu có độ trong suốt (bao gồm cả kênh alpha).
    - Vì là ảnh đã qua tiền xử lý thành ảnh trắng đen nên chọn flag = 2 để có độ chính xác cao nhất.
    ```python
    #read image file.
    open_path_fname = "C:\\MyFolder\\Code\\Python\\img\\week1.png"
    img = cv2.imread(open_path_fname,2)
    ```
    - **Lưu ý:** *vì cách sắp xếp file mỗi máy là khác nhau chỉnh nên nhớ sửa lại đường dẫn và tên file trên biến path_fname trước khi chạy code*
    - Nhược điểm khi xài flag =2 là ảnh trắng đen nên lúc sau khi vẽ viền bằng lệnh drawContours() sẽ không thấy được màu của đường viền.
    - Khắc phục bằng cách input thêm 1 ảnh nữa flag = 1 để lúc sau vẽ đường viền lên.
    ```python
    img_draw = cv2.imread(open_path_fname,1)
    ```
3. Tiền xử lý ảnh:
    - Chuyển ảnh thành ảnh grayscale:
    ```python
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ```
    - Làm mịn ảnh, khử nhiễu:
    ```python
    img_blur = cv2.GaussianBlur(img_gray,(3,3), 0)
    ```
    - ***Lưu ý:*** *Do ảnh đầu vào đã được tiền xử lý nên bỏ qua các bước tiền xử lý trên*
4. Xác định viền của hạt nước:
    - Có 2 hướng xác định viền:
        - Hướng 1: dùng hàm cv2.Canny():
        ```python
        cv2.Canny(img, min_val, max_val)
        ```
        - Hướng 2: dùng hàm cv2.Threshold():
        ```python
        cv2.Threshold(img, min_val, max_val, cv2.THRESH_BINARY)
        ```
    - Do ảnh input là ảnh đã qua tiền xử lý trắng đen, và ảnh có nhiều chi tiết và mật độ chi tiết cao, các hạt chồng chéo lên nhau nên phương pháp Canny tỏ ra hiệu quả hơn và cho độ chính xác cao hơn phương phápThreshold.
    - ***chọn phương pháp Canny***
    ```python
    #Canny edge direction.
    threshold = 0
    edges = cv2.Canny(img, threshold, threshold*2)
    ```
    - **Chú thích:** *thông thường giá trị max_val = 2 min_val, do ảnh đã qua xử lý rất chính xác nên chọn mức min_val thấp nhất để không bỏ sót bất kì giọt li ti nào.*
    - Ta thu được ảnh:
    <div align='center'>
    <img src="img\edges.png" width='90%'>
    </div>
    - Zoom ảnh lên:
    <div align='center'>
    <img src="img\zoomEdges.png" width='90%'>
    </div>
5. Tìm viền của hạt nước để tính toán:
    - Sử dụng hàm cv2.findContours() để tìm viền của đối tượng
    ```python
    # get contours list
    contours, _ = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ```
    - Ta thu được 1 list “contours” bao gồm tất cả các đường viền của tất cả các giọt nước trong ảnh.
6. Số lượng hạt nước tìm được (tương đối):
    - Theo lý thuyết thì nếu không có sai sót thì cứ một giọt nước sẽ có 1 đường viền bao quanh.
    - Suy ra số lượng hạt nước cũng chính là số lượng viền của hạt nước.
    - Dùng làm len() để đếm số đường viền có trong list “contours” và in ra màn hình bằng lệnh print()
    ```python
    #print number of drops
    total = len(contours)
    print("number of drops in the image : ", total)
    #total = 47233
    ```
    - **Số lượng hạt nước thu được là: 47233 hạt**
7. Kiểm nghiệm độ chính xác của số liệu:
    - **Vẽ đường bao quanh giọt nước để xem tính chính xác của việc đếm hạt**
    - Có 5 kiểu vẽ đường bao:
        - Contours (bao theo đường viền của hạt)
            <div align='center'>
            <img src="img\contours.png" width='90%'>
            </div>
        - Normal Rectangle (bao hình chữ nhật đứng bọc toàn bộ hạt) (Bao hình chữ nhật màu xanh)
            <div align='center'>
            <img src="img\boundingrect.png" width='90%'>
            </div>
        -  Rotated Rectangle (bao hình chữ nhật bọc toàn bộ hạt có diện tích nhỏ nhất)(Bao hình chữ nhật màu đỏ)
            <div align='center'>
            <img src="img\boundingrect.png" width='90%'>
            </div>
        - Minimum Enclosing Circle (bao hình tròn có đường kính là 2 điểm xa nhất trên hạt)
            <div align='center'>
            <img src="img\circumcircle.png" width='90%'>
            </div>
        - Fitting an Ellipse (bao hình ellipse tương đối vừa với hạt)
            <div align='center'>
            <img src="img\fitellipse.png" width='90%'>
            </div>
    - Bao kiểu Rotated Rectangle là tối ưu nhất vì:
        - Trông gần giống nhất với hình dạng hạt nước.
        - Đảm bảo sự nổi bật và tách biệt khi chồng chéo nhiều hình lên nhau
        - Điều kiện để vẽ đơn giản hơn Ellipse (một số hạt quá nhỏ không đủ điều kiện để code bao theo Ellipse)
        - Chiều rộng của hình chữ nhật cũng xấp xỉ với đường kính hạt nước (ta có thể tận dụng để làm Task2)
    - Cách vẽ đường bao Rotated Rectangle cho mỗi hạt:
    ```python
    # draw Rotated Rect bounding for drop
    def drawBoundingRect(contour):
        # get the min area rect
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box) #convert all coordinates floating point value to int
        # draw all contours
        cv2.drawContours(img_draw, [box], 0, (0, 255, 0), 1)
    ```
    - Cho vào vòng lặp for để vẽ đường bao hình chữ nhật cho tất cả các hạt:
    ```python
    for cnt in contours :
        drawBoundingRect(cnt)
    ```
    - Dùng hàm cv2.imshow() để hiển thị hình đã vẽ ra màn hình:
    ```python
    #show image on display.
    cv2.imshow("Bounding Rectangle of Drops", img_draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ```
    - Dùng hàm cv2.imwrite() để lưu ảnh lại để tiện cho việc xem lại, zoom in, zoom out:
    ```python
    #save as image.
    save_path = "C:\\MyFolder\\Code\\Python\\img\\week1Task1result.png"
    cv2.imwrite(save_path, img_draw)
    ```
    - Ảnh thu được sau khi lưu:
    <div align='center'>
    <img src="img\week1Task1result.png" width='90%'>
    </div>
    - Zoom ảnh lên, ta thấy:
    <div align='center'>
    <img src="img\zoomTask1result.png" width='90%'>
    </div>
        - Đối với các hạt nhỏ và các hạt phía xa thì tương đối chính xác và hiệu quả.
    <div align='center'>
    <img src="img\zoomTask1resultNear.png" width='90%'>
    </div>
        - Đối với các hạt gần tâm thì còn nhiều sai sót: Nhiều hạt bị chồng chéo, bị dính với nhau trên ảnh chụp thì vẫn bị tính là một vật thể.
    - **Kết quả:** *Còn nhiều sai số, không xác định được chính xác số hạt bắn ra.*
## **IV. Task 2: Tìm phân bố hạt trong ảnh với tỉ lệ 10 micron = 1 pixel**
1. Reset lại img_draw để vẽ cho Task 2:
    ```python
    img_draw = cv2.imread(open_path_fname,1)
    ```
2. Khoanh vùng đối tượng (ROI):
    - Vùng ảnh được chia làm 3 vùng: cận tâm, trung bình, xa tâm.
    - Giả thiết một hạt nước đi từ vùng cận tâm ra đến xa tâm. Ở các vùng thì số lượng hạt và mật độ hạt là như nhau (vì chúng chỉ di chuyển từ vùng này sang vùng khác). Khác nhau về vận tốc hạt còn số lượng và kích thước hạt gần như là không đổi.
    - Vùng cận tâm có số lượng hạt nước chồng lấn cao nhất, nên bỏ qua không xét đến.
    - Do đó thực ra chỉ cần đo ở vùng trung bình hoặc xa tâm là có thể biết số hạt nước chính xác khi chúng tách rời nhau ra, dễ nhận diện nhất.
    - ***Chọn vùng xa tâm để dễ xét***
    - Vùng quan tâm bây giờ chỉ là vùng xa tâm. Ta sẽ che vùng gần tâm và trung bình đi.
    - **Vẽ hình tròn đen để che đi các hạt nước ở những vùng không xét đến này**
    - Hình tròn có tâm xấp xỉ bằng tâm tấm ảnh( di dời cho hợp lý), bán kính hình tròn sao cho số hạt đếm được chỉ còn lại 1/3 tổng số hạt đã tìm ở trên( xấp xỉ 12408).
    - Sau nhiều lần thử nghiệm thì đường kính 1291 cho số lượng hạt là 12423 gần đúng với số hạt 12408 nhất.
    ```python
    #draw black circle (find ROI).
    height, width = img.shape
    center = (int(width/2-120), int(height/2-350))
    radius = 1391
    black_circle = cv2.circle(img, center, radius, (0,0,0), -1 )
    ```
3. Xác định viền, tìm viền, số lượng hạt đếm được:
    - Giống như Task 1.
    - Để thử nghiệm xem bán kính nào của hình tròn đen thì số hạt còn lại xấp xỉ 1/3 tổng số hạt đã tính ở Task 1.
    - Để xác định list contours mà chạy vòng lặp
4. Đổi đơn vị:
    - tạo 1 biến đổi đơn vị micron để khi tính bằng đơn vị pixel thì nhân với biến để thành đơn vị micron
    ```python
    microns = 10 #10 microns per pixel
    ```
5. Tìm đường kính hạt
    - Chiều rộng của vệt nước chính là đường kính thực của hạt nước đang chuyển động với tận tốc lớn. chiều rộng này bằng chính chiều rộng của đường bao hình chữ nhật.
    - Sử dụng hàm cv2.minAreaRect() để xác định chiều rộng này.
    - Nhưng hàm cv2.minAreaRect() chỉ có thể trả về độ dài 2 cạnh dưới dạng chiều cao và chiều ngang thay vì chiều rộng và chiều dài nên ta phải xài hàm điều kiện if else để xác định chính xác chiều rộng của đường bao hình chữ nhật.
    - Tạo 1 list để lưu tất cả giá trị đường kính hạt và chạy vòng lặp để nhập đường kính của từng hạt vào list đó.
    ```python
    diameter_list = []
    for cnt in contours :   
        drawBoundingRect(cnt)
        ((x,y),(width_rect,height_rect),angle)= cv2.minAreaRect(cnt)
        if width_rect < height_rect:
            diameter = width_rect*microns
        else:
            diameter = height_rect*microns
        diameter_list.append(diameter)
    ```
    - **Ghi nhớ** *dùng drawBoundingRect() vẽ đường bao hình chữ nhật để lúc sau kiểm nghiệm tính chính xác của số liệu*
6. Xác định kích thước lớn nhất của hạt:
    - Sử dụng hàm max() để xác định đường kính lớn nhất trong list đường kính.
    ```python
    #find max diameter to use for loop
    max_diameter = max(diameter_list)
    print("max diameter:",max_diameter) #max diameter = 258.17
    ```
    - **Đường kính lớn nhất ta thu được là: 258.17**
7. Xác định phân bố hạt theo đường kính:
    - Làm tròn kích thước hạt lớn nhất lên hàng chục (làm tròn 258.17 lên 260) để chia nhóm phân bố hạt theo đường kính đơn vị là 10 micron:
    - Do Python không có hàm roundup() như Excel có thể làm tròn đến hàng chục mà chỉ có hàm math.ceil() làm tròn đến hàng đơn vị nên ta sẽ tận dụng hàm này để tạo 1 cái function như hàm roundup() trong Excel
    ```python
    def roundUp(n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier
    ```
    - Chia toàn bộ hạt vào 26 nhóm, mỗi nhóm bao gồm các hạt có đường kính chênh lệch nhau dưới 10 micron: ví dụ: nhóm đường kính từ 0 đến dưới 10, nhóm đường kính từ 10 đến dưới 20,.... cho đến nhóm đừng kính từ 250 đến dưới 260.
    - Ta tạo một cái dictionary để lưu dữ liệu song song nhóm đường kính và số hạt.
    ```python
    #data number/diameter of drops
    size_num_drops = {}
    ```
    - Rồi chạy 2 vòng lặp lồng vào nhau:
        - vòng trong dùng để đếm số hạt trong mỗi nhóm.
        - vòng lặp ngoài dùng để dữ liệu vào dictionary.
    ```python
    # input data to num/diameter dict
    count = 0
    min_val = 0
    for max_val in range(microns,int(roundUp(max_diameter,-1)+microns),microns):
        for diameter in diameter_list:
            if diameter >= min_val and diameter < max_val:
                count += 1
        size_num_drops[str(max_val)]=count
        count = 0
        min_val = max_val
    ```
8. Vẽ biểu đồ phân bố:
    - Chuyển dữ liệu từ dictionary thành list để vẽ biểu đồ:
    ```python
    size_drops = list(size_num_drops.keys())
    num_drops = list(size_num_drops.values())
    ```
    - Do chia theo nhóm nên biểu đồ hiển thị rõ ràng và tối ưu nhất là biểu đồ cột
    - Sử dụng hàm plt.bar() của thư viện matplotlib để vẽ biểu đồ.
    ```python
    fig = plt.figure(figsize = (10, 5))
    plt.bar(size_drops, num_drops, color = 'maroon',width =0.9)
    plt.title('Distribution of drops')
    plt.xlabel('Under size of drops (micron)')
    plt.ylabel('Number of drops')
    plt.show()
    ```
    <div align='center'>
    <img src="img\Diagram.png" width='90%'>
    </div>
    - Nhận xét: Từ đồ thị của vùng xa tâm, ta thấy các hạt phân bố tập trung ở kích thước từ 0 đến 150 micron. Phân bố nhiều nhất ở kích thước từ 20 đến dưới 30 micron. Kế đến là các vùng từ 0 đến dưới 10 micron và từ 40 đến dưới 50 micron.
9. Kiểm nghiệm tính chính xác của số liệu:
    - Khi tìm đường kính hạt ta đã dùng drawBoundingRect() để vẽ đường bao.
    - Hiển thị hình vẽ ra màn hình bằng lệnh cv2.imshow() và lưu ảnh lại để tiện cho việc xem lại, zoom in zoom out (tương tự như Task 1)
    - **Lưu ý:** *đặt tên file ảnh khác Task 1*
    ```python
    #save as image.
    save_path = "C:\\MyFolder\\Code\\Python\\img\\week1Task2result.png"
    cv2.imwrite(save_path, img_draw)

    #show image on display.
    cv2.imshow("Bounding Rectangle of Drops", img_draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ```
    - Ảnh thu được sau khi lưu:
    <div align='center'>
    <img src="img\week1Task2result.png" width='90%'>
    </div>
    - Zoom ảnh lên, ta thấy:
    <div align='center'>
    <img src="img\zoomTask2result.png" width='90%'>
    </div>
    - Nhận xét: hạt nước nằm trên đường tròn ROI bị chia đôi kích thước, nếu chiều dài sau khi bị chia đôi < chiều rộng thì sẽ xảy ra sai số. Nhưng nhìn chung sai số là khá nhỏ và không đáng kể so với phần ta xét.
## **V. Tài liệu tham khảo:**
1. https://phamdinhkhanh.github.io/2020/01/06/ImagePreprocessing.html
2. https://answers.opencv.org/question/59391/multiple-objects-classification/
3. https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
4. https://www.geeksforgeeks.org/count-number-of-object-using-python-opencv/
5. https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
6. https://theailearner.com/tag/angle-of-rotation-by-cv2-minarearect/
7. https://theailearner.com/tag/cv2-minarearect/#:~:text=minAreaRect()%20for%20finding%20the,)%2C%20angle%20of%20rotation).
8. https://learnopencv.com/edge-detection-using-opencv/
