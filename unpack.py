import os,sys
from PIL import Image


def get_img_item_list(filename):
    """
    获得图片列表
    :param filename:
    :return:
    """
    f = open(filename, 'r')
    lines = f.readlines()
    print(len(lines))
    image_name = lines[1]
    print("图片名称: " + image_name)
    image_num = int((len(lines) - 6) / 7)
    print("拆分图片个数: " + str(image_num))
    item_list = []
    for i in range(image_num):
        item = {}
        group_index = i * 7
        item['name'] = lines[group_index + 6].strip()
        item['rotate'] = lines[group_index + 7].split(':')[1].strip()
        item['xy'] = lines[group_index + 8].split(':')[1].strip()
        item['size'] = lines[group_index + 9].split(':')[1].strip()
        item['orig'] = lines[group_index + 10].split(':')[1].strip()
        item['offset'] = lines[group_index + 11].split(':')[1].strip()
        item['index'] = lines[group_index + 12].split(':')[1].strip()

        item_list.append(item)

    return item_list


def gen_new_img(item_list, img_file, out_dir):
    """
    生成新图片
    :param item_list:
    :param img_file:
    :param out_dir:
    :return:
    """
    big_image = Image.open(img_file)
    for item in item_list:
        name = item['name']
        is_rotate = item['rotate'] == 'true'
        x = int(item['xy'].split(',')[0].strip())
        y = int(item['xy'].split(',')[1].strip())
        w = int(item['size'].split(',')[0].strip())
        h = int(item['size'].split(',')[1].strip())
        ow = int(item['orig'].split(',')[0].strip())
        oh = int(item['orig'].split(',')[1].strip())
        # 旋转处理
        if is_rotate:
            temp = w
            w = h
            h = temp

        box = [x, y, x + w, y + h]
        rect_on_big = big_image.crop(box)
        # rect_on_big.show()

        if is_rotate:
            rect_on_big = rect_on_big.rotate(-90, expand=True)

        result_image = Image.new('RGBA', (ow, oh), (0, 0, 0, 0))

        result_image.paste(rect_on_big)
        print(item)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        outfile = (out_dir + name + '.png')
        result_image.save(outfile)


def unpack(file_dir):
    """
    拆分指定目录下图集
    :param file_dir:
    :return:
    """
    cwd = file_dir
    path = os.listdir(cwd)
    for p in path:
        d = os.path.splitext(p)
        file_name = d[0]
        file_suffix = d[1]
        if file_suffix == '.atlas':
            # 找png 如果有则切图
            img_file = os.path.join(cwd, file_name + '.png')
            print(img_file)
            if os.path.exists(img_file):
                # 拆图
                # item_list = readFile()
                atlas_file = os.path.join(cwd, p)
                item_list = get_img_item_list(atlas_file)
                out_dir = os.path.join(cwd, 'out', file_name, '')
                gen_new_img(item_list, img_file, out_dir)
            else:
                print('找不到对应png')


if __name__ == '__main__':

    #dir_0 = sys.argv[0]

    # 当前目录
    dir1 = os.getcwd()
    unpack(dir1)

    # 当前目录下img目录
    dir2 = os.path.join(os.getcwd(),'img')
    if os.path.exists(dir2):
        unpack(dir2)



