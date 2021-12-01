\ Model sspwp
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 d[1,2] + 0 d[1,3] + 0 d[2,1] + 0 d[2,3] + 0 d[3,1] + 0 d[3,2] + 0 l[1,2]
   + 0 l[1,3] + 0 l[2,1] + 0 l[2,3] + 0 l[3,1] + 0 l[3,2] + 0 x[1] + 0 x[2]
   + 0 x[3] + 0 y[1] + 0 y[2] + 0 y[3] + h_max + 0 px[1] + 0 px[2]
   + 0 px[3] + 0 yh[1] + 0 yh[2] + 0 yh[3] + pxf[1] + pxf[2] + pxf[3]
Subject To
Bounds
Binaries
 d[1,2] d[1,3] d[2,1] d[2,3] d[3,1] d[3,2] l[1,2] l[1,3] l[2,1] l[2,3]
 l[3,1] l[3,2]
General Constraints
 max_height: h_max = MAX ( yh[1] , yh[2] , yh[3] )
 abspx1: pxf[1] = ABS ( px[1] )
 abspx2: pxf[2] = ABS ( px[2] )
 abspx3: pxf[3] = ABS ( px[3] )
End
