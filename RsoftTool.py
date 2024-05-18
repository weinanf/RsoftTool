class RsoftTool:
    """Rsoft工具类"""
    
    """暂不定义构造函数，默认空构造函数"""

    """"""
    
    def getSymbolValue(self, file_path, symbol):
        result = 0
        with open(file_path, 'r') as file:
            line = file.readline()
            while line:
                if line.split('=')[0].strip() == symbol:
                    result = float(line.split('=')[1].strip())
                    break
                line = file.readline()
        return result
    
    def setSymbolValue(self, file_path, file_path_new, symbol, symbol_value):
        lines = []
        with open(file_path, 'r') as file:
            line = file.readline()
            while line:
                if line.split('=')[0].strip() == symbol:
                    lines.append(line.split('=')[0]+"= "+str(symbol_value)+"\n")
                else:
                    lines.append(line)
                line = file.readline()
        with open(file_path_new, 'w') as file:#'a'表示追加,'w'表示覆盖写入
            file.writelines(lines)
    
    def appendLinesToFile(self, file_path, lines):
        #这个函数用来将新的component追加到ind文件中
        with open(file_path, 'a') as file:#'a'表示追加
            file.writelines(lines)
    
    def getMaxSegmentIndex(self,file_path):
        maxIndex = 0
        with open(file_path, 'r') as file:
            line = file.readline()
            while line:
                if line.split(' ')[0].strip() == "segment" or line.split(' ')[0].strip() == "time_monitor":
                    maxIndex = int(line.split(' ')[1].strip())
                line = file.readline()
        return maxIndex
    
    def drawPixelsFromArray(self,temp_file,array):
        if len(array)!=(self.getSymbolValue(temp_file,"Num_pixel_x")*self.getSymbolValue(temp_file,"Num_pixel_y")):
            #判断当前数组大小是否和像素总个数匹配，如不匹配则立即停止
            print("Array doesn't match pixel nums!")
            raise SystemExit #中断程序
        maxSegmentIndex = self.getMaxSegmentIndex(temp_file)
        count = 0
        for i in range(0,int(self.getSymbolValue(temp_file,"Num_pixel_x")),1):
            for j in range(0,int(self.getSymbolValue(temp_file,"Num_pixel_y")),1):
                    #print(str(i)+","+str(j))
                    if array[i*int(self.getSymbolValue(temp_file,"Num_pixel_x"))+j] == 1:
                        #构建segment的字符串数组
                        lines= []
                        lines.append("segment "+str(maxSegmentIndex+count+1)+"\n")
                        count = count+1
                        lines.append("\t"+"priority = 1"+"\n")
                        lines.append("\t"+"comp_name = pixel_"+str(i)+"_"+str(j)+"\n")
                        lines.append("\t"+"extended = 1"+"\n")
                        lines.append("\t"+"begin.x = -Width_x/2+Width_pixel_x/2+Width_pixel_x*"+str(i)+"\n")
                        lines.append("\t"+"begin.z = -Width_y/2+Width_pixel_y*"+str(j)+"\n")
                        lines.append("\t"+"begin.width = Width_pixel_x"+"\n")
                        lines.append("\t"+"end.x = -Width_x/2+Width_pixel_x/2+Width_pixel_x*"+str(i)+"\n")
                        lines.append("\t"+"end.z = -Width_y/2+Width_pixel_y+Width_pixel_y*"+str(j)+"\n")
                        lines.append("\t"+"end.width = Width_pixel_x"+"\n")
                        lines.append("\t"+"mat_name = Air"+"\n")
                        lines.append("end segment"+"\n")
                        #将当前的lines追加到临时文件中
                        self.appendLinesToFile(temp_file,lines)

    def drawPixelsFromArray3D(self, temp_file, array):
        if len(array)!=(self.getSymbolValue(temp_file,"Num_x")*self.getSymbolValue(temp_file,"Num_y")):
            #判断当前数组大小是否和像素总个数匹配，如不匹配则立即停止
            print("Array doesn't match pixel nums!")
            raise SystemExit #中断程序
        maxSegmentIndex = self.getMaxSegmentIndex(temp_file)
        count = 0
        for i in range(0,int(self.getSymbolValue(temp_file,"Num_x")),1):
            for j in range(0,int(self.getSymbolValue(temp_file,"Num_y")),1):
                    #print(str(i)+","+str(j))
                    if array[i*int(self.getSymbolValue(temp_file,"Num_x"))+j] == 1:
                        #构建segment的字符串数组
                        lines= []
                        lines.append("segment "+str(maxSegmentIndex+count+1)+"\n")
                        count = count+1
                        lines.append("\t"+"priority = 1"+"\n")
                        lines.append("\t"+"comp_name = pixel_"+str(i)+"_"+str(j)+"\n")
                        lines.append("\t"+"extended = 1"+"\n")
                        lines.append("\t"+"begin.x = -W_x/2+W_pixel_x/2+W_pixel_x*"+str(i)+"\n")
                        lines.append("\t"+"begin.y = -W_y/2+W_pixel_y/2+W_pixel_y*"+str(j)+"\n")
                        lines.append("\t"+"begin.z = -H"+"\n")
                        lines.append("\t"+"begin.height = W_pixel_y"+"\n")
                        lines.append("\t"+"begin.width = W_pixel_x"+"\n")
                        lines.append("\t"+"end.x = -W_x/2+W_pixel_x/2+W_pixel_x*"+str(i)+"\n")
                        lines.append("\t"+"end.y = -W_y/2+W_pixel_y/2+W_pixel_y*"+str(j)+"\n")
                        lines.append("\t"+"end.z = 0"+"\n")
                        lines.append("\t"+"end.height = W_pixel_y"+"\n")
                        lines.append("\t"+"end.width = W_pixel_x"+"\n")
                        lines.append("\t"+"mat_name = Air"+"\n")
                        lines.append("end segment"+"\n")
                        #将当前的lines追加到临时文件中
                        self.appendLinesToFile(temp_file,lines)

        

class Data1dSingle:
    """存储一维数据的类。amplitude,real,imag等实数。"""
    """属性"""
    size = 0 #数组大小
    min_x = 0 #最小坐标
    max_x = 0 #最大坐标
    wavelength = 0 #波长
    data = [] #存储数据的一维数组
    file_path = "" #源文件的绝对路径
    max_value = 0
    min_value = 0
    grid_size = 0
    sum_value = 0

    """构造函数"""
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as file:
            line = file.readline() #读取第一行 无用的信息
            line = file.readline() #读取第二行
            second_line = line.split()
            self.size = int(second_line[0])
            self.min_x = float(second_line[1])
            self.max_x = float(second_line[2])
            self.grid_size = (self.max_x-self.min_x)/(self.size-1)
            self.wavelength = float(second_line[5].split('=')[1])
            data = []
            line = file.readline()#继续读取第三行，开始读取数据
            while line:
                line_data = line.replace('\n', '')
                self.data.append(float(line_data))
                line = file.readline()
        self.max_value = max(self.data)
        self.min_value = min(self.data)
        self.sum_value = sum(self.data)

class Data2dSingle:
    """存储一维数据的类。amplitude,real,imag等实数。"""
    """属性"""
    size_x = 0 #x维度大小
    size_y = 0 #y维度大小
    min_x = 0 #x最小坐标
    max_x = 0 #x最大坐标
    max_y = 0
    min_y = 0
    wavelength = 0 #波长
    #line = [] #存储数据的一维数组
    lines = []
    file_path = "" #源文件的绝对路径
    max_value = 0
    min_value = 0
    grid_size_x = 0
    grid_size_y = 0
    sum_value = 0

    """构造函数"""
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as file:
            line = file.readline() #读取第1行 无用
            line = file.readline() #读取第2行 无用
            line = file.readline() #读取第3行 横轴的信息
            line = line.split()
            self.size_x = int(line[0])
            self.min_x = float(line[1])
            self.max_x = float(line[2])
            self.grid_size_x = (self.max_x-self.min_x)/(self.size_x-1)
            self.wavelength = float(line[5].split('=')[1])
            line = file.readline() #读取第4行 纵轴的信息
            line = line.split()
            self.size_y = int(line[0])
            self.min_y = float(line[1])
            self.max_y = float(line[2])
            self.grid_size_y = (self.max_y-self.min_y)/(self.size_y-1)
            self.lines = []
            line = file.readline()#继续读取第5行，开始读取数据
            while line:
                line_data = line.replace('\n', '').split()
                self.lines.append([float(individual) for individual in line_data])
                line = file.readline()
        self.sum_value = sum([sum(individual) for individual in self.lines])
        self.max_value = max([max(individual) for individual in self.lines])
        self.min_value = min([min(individual) for individual in self.lines])

