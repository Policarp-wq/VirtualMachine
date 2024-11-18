import os


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        if self.log_file is None:
            return
        f = open(self.log_file, 'a')

        f.write('<log>\n')
        f.close()

    def log(self, tag, msg):
        if self.log_file is None:
            return
        with open(self.log_file, 'a') as f:
            f.write(f'  <{tag}>{msg}</{tag}>\n')

    def log_bytes(self, tag, bytes):
        if self.log_file is None:
            return
        with open(self.log_file, 'a') as f:
            f.write(f'  <{tag}>\n')
            for byte in bytes:
                f.write(f'      <hex>{byte}</hex>\n')
            f.write(f'  </{tag}>\n')

    def stop(self):
        if self.log_file is None:
            return
        f = open(self.log_file, 'a')
        f.write('</log>\n')
        f.close()
        print('Log saved to ', os.path.abspath(self.log_file))

# слева направо
