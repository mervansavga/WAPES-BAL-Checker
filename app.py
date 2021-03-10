from bottle import route, run, request, static_file
import os
import tempfile
import shutil
import bal_checker
import tracemalloc
#app = Bottle()

@route('/')
def root():
    return static_file('test.html', root='.')

@route('/upload', method='POST')
def do_upload():
    tracemalloc.start()
    page1 = request.files.get('page1')
    page2 = request.files.get('page2')
    position = request.forms.get('position')

    name, ext = os.path.splitext(page1.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    name2, ext2 = os.path.splitext(page2.filename)
    if ext2 not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    temp_path = tempfile.mkdtemp()
    #save_path = "./tmp/{folder}".format(folder=temp_folder)
    # if not os.path.exists(save_path):
    #     os.makedirs(save_path)

    file1_path = "{path}/{file}".format(path=temp_path, file=page1.filename)
    page1.save(file1_path)
    file2_path = "{path}/{file}".format(path=temp_path, file=page2.filename)
    page2.save(file2_path)
    file_list = [file1_path, file2_path]
    print(file_list)
    # snapshot1 = tracemalloc.take_snapshot()
    cevap = bal_checker.bal_checker(file_list, position)
    shutil.rmtree(temp_path)
    
    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics('traceback')

    # # pick the biggest memory block
    # stat = top_stats[0]
    # print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
    # for line in stat.traceback.format():
    #     print(line)
    # #return "File successfully saved to '{0}'.".format(save_path)
    return cevap

run(server='paste',host='165.22.84.2', port=5000, debug=True)
