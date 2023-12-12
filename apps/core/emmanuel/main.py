
from loader import _curva, _cronograma
import time 
import os

bl_id = 1
bl_root_path = r'data\to_push\cronogramas\contratadas\mip\baseline'
bl_path = os.path.join(bl_root_path, str(bl_id))

root_dir = r'data\to_push\cronogramas\contratadas\mip\avanco'
output_dir = r'data\updates\output\mip'


t_start = time.time()
for file_id in os.listdir(root_dir):
    print('Processing folder :',file_id, '\n', '#'*30)
    root_path = os.path.join(root_dir, str(file_id))
    for file_name in os.listdir(root_path):
        file_path = os.path.join(root_path, file_name)
        if '.xer' in file_name:
            _cronograma(file_path, file_id, bl_path, output_dir) #função chama a carga do cronograma
            pass
        if '.xlsx' in file_name:
            _curva(file_path, file_id, bl_path, output_dir) #função chama a carga da curva
            pass
    print('\n')


print('Tempo de execução: ', (time.time() - t_start)/60)