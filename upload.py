from lib import btpeer
# print btpeer

if __name__ == '__main__':
    node = btpeer.BTPeer(5, 5555)
    node.debug = True
    node.mainloop()
