import global_values as g_v

def filter_controller():
  while 1:
    g_v.e1.wait()
    g_v.e1.clear()
    # print('filter thread is started')
  ##--------------------------------------------
  ##----filtration for every single section-----
  ##--------------------------------------------

    g_v.X = filter(1, 1, g_v.a_coef_1_1, g_v.b_coef_1_1, 2, g_v.X)
    # g_v.Y = 0
    g_v.X = filter(1, 2, g_v.a_coef_1_2, g_v.b_coef_1_2, 2, g_v.X)
    # g_v.Y = 0
    g_v.X = filter(1, 3, g_v.a_coef_1_3, g_v.b_coef_1_3, 1, g_v.X)
    # g_v.Y = 0

    g_v.X = filter(2, 1, g_v.a_coef_2_1, g_v.b_coef_2_1, 2, g_v.X)
    # g_v.Y = 0
    g_v.X = filter(2, 2, g_v.a_coef_2_2, g_v.b_coef_2_2, 2, g_v.X)
    # g_v.Y = 0
    g_v.X = filter(2, 3, g_v.a_coef_2_3, g_v.b_coef_2_3, 2, g_v.X)
    # g_v.Y = 0

    g_v.X = filter(3, 1, g_v.a_coef_3_1, g_v.b_coef_3_1, 2, g_v.X)
    # g_v.Y = 0
    g_v.X = filter(3, 2, g_v.a_coef_3_2, g_v.b_coef_3_2, 2, g_v.X)
    # g_v.Y = 0
    g_v.X = filter(3, 3, g_v.a_coef_3_3, g_v.b_coef_3_3, 2, g_v.X)
    # g_v.Y = 0
    g_v.filt_volt.append(g_v.X)
    g_v.e2.set()
    # print('filter thread is finished')
##--------------------------------------------------------
##--------------------filtering part----------------------
##-------------------------------------------------------
def filter(stage_n, sec_n, a_coef, b_coef, n_coef, input_data):
  Y = 0## zeroize the first state of filter data
  for m in range(n_coef, 0, -1):
      g_v.Z[stage_n - 1][sec_n - 1][m] = g_v.Z[stage_n - 1][sec_n - 1][m - 1]

  g_v.Z[stage_n - 1][sec_n - 1][0] = input_data*a_coef[0]

  for j in range (1, n_coef + 1, 1): 
      g_v.Z[stage_n - 1][sec_n - 1][0] += -g_v.Z[stage_n - 1][sec_n - 1][j]*a_coef[j]

  for k in range (0, n_coef + 1, 1):
      Y += g_v.Z[stage_n - 1][sec_n - 1][k]*b_coef[k]
  return Y