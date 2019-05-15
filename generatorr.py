import global_values as g_v

##--------thread for signal generaton--------
def generator():
  for i in range (len(g_v.voltage)):
    g_v.e2.wait()
    # print('generator thread is started')
    g_v.e2.clear()
    g_v.X = g_v.voltage[i]
    # print(i , X)
    g_v.e1.set()
    # print('generator thread is finished')