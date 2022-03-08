#--- GLOBAL PARAMETERS ---#

arh = 5
arw = 2.*arh
arr_size = 2.*arw
space = 5
chanels = 10
size_ini = 200

# Colors
col_arh = color(128,0,255)
col_arv_down = color(255,0,128)
col_arv_up = color(0,128,0)
col_longar = color(128,128,128)
col_layer = color(0,128,255)
col_layconc = color(0,255,255)


#--- FUNCTIONS ---#

# Shapes

def arrow(x,y):
    rectMode(CORNER)
    rect(x,y-arh/2.,arw,arh)
    triangle(x+arw,y-arh,x+arw,y+arh,x+arr_size,y)

def arrow_horizontal(x,y,col):
    fill(col/2.)
    arrow(x+space/2.,y+space/2.)
    fill(col)
    arrow(x,y)

def arrow_vertical(x,y,sign,col):
    # Shadow
    fill(col/2.)
    pushMatrix()
    translate(x+space/2.,y+space/2.)
    rotate(sign*PI/2.)
    arrow(0,0)
    popMatrix()
    # Arrow
    fill(col)
    pushMatrix()
    translate(x,y)
    rotate(sign*PI/2.)
    arrow(0,0)
    popMatrix()

def long_arrow(x,y,x2):
    arh2, arw2, arr_size2 = 2.*arh, 2.*arw, 2.*arr_size
    rectMode(CORNER)
    # Shadow
    x_ini, y_ini, x_fin = x+space/2., y+space/2., x2+space/2.
    fill(col_longar/2.)
    rect(x_ini,y_ini-arh2/2.,x_fin-x-arw2,arh2)
    triangle(x_fin-arw2,y_ini-arh2,x_fin-arw2,y_ini+arh2,x_fin,y_ini)
    # Arrow
    x_ini, y_ini, x_fin = x, y, x2
    fill(col_longar)
    rect(x_ini,y_ini-arh2/2.,x_fin-x-arw2,arh2)
    triangle(x_fin-arw2,y_ini-arh2,x_fin-arw2,y_ini+arh2,x_fin,y_ini)

def layer(x,y,wid,siz,col):
    rectMode(CENTER)
    fill(col/2.)
    rect(x+space/2.,y+space/2.,wid,siz)
    fill(col)
    rect(x,y,wid,siz)

# Distances

def dist_layers(chanels_in,chanels_out):
    return chanels_in/2 + arr_size + 2.*space + chanels_out/2.

def dist_vert(size_ini):
    return size_ini/2. + 2.*space + arr_size + size_ini/2./2.

# Blocks

def block(x_ini,y_ini,chanels_in,chanels_mid,chanels_out,size_ini):
    lay2 = x_ini + dist_layers(chanels_in,chanels_mid)
    lay3 = lay2 + dist_layers(chanels_mid,chanels_out)
    layer(x_ini,y_ini,chanels_in,size_ini,col_layer)
    arrow_horizontal(x_ini+chanels_in/2+space,y_ini,col_arh)
    layer(lay2,y_ini,chanels_mid,size_ini,col_layer)
    arrow_horizontal(lay2+chanels_mid/2+space,y_ini,col_arh)
    layer(lay3,y_ini,chanels_out,size_ini,col_layer)

def contracting_block(x_ini,y_ini,chanels_in,chanels_out,size_ini):
    lay2 = x_ini + dist_layers(chanels_in,chanels_out)
    lay3 = lay2 + dist_layers(chanels_out,chanels_out)
    block(x_ini,y_ini,chanels_in,chanels_out,chanels_out,size_ini)
    arrow_vertical(lay3,y_ini+size_ini/2.+space,1.,col_arv_down)
    write_label(x_ini,y_ini,chanels_in,size_ini,"left")
    write_label(lay2,y_ini,chanels_out,size_ini,"left")
    write_label(lay3,y_ini,chanels_out,size_ini,"left")
    
def expanding_block(x_ini,y_ini,chanels_in,chanels_mid,chanels_out,size_ini):
    lay2 = x_ini + dist_layers(chanels_in,chanels_mid)
    lay3 = lay2 + dist_layers(chanels_mid,chanels_out)
    block(x_ini,y_ini,chanels_in,chanels_mid,chanels_out,size_ini)
    arrow_vertical(lay3,y_ini-size_ini/2.-space,-1.,col_arv_up)
    write_label(x_ini,y_ini,chanels_in,size_ini,"right")
    write_label(lay2,y_ini,chanels_mid,size_ini,"right")
    write_label(lay3,y_ini,chanels_out,size_ini,"right")

def concat_block(x_ini,y_ini,x_end,chanels_in,chanels_out,sizelay):
    long_arrow(x_ini+chanels_in/2+2*space,y_ini,x_end-chanels_out/2.-space-chanels_in)
    layer(x_end-chanels_out+chanels_in/2,y_ini,chanels_in,sizelay,col_layconc)
    write_label(x_end-chanels_out/2.,y_ini,chanels_in,sizelay,"up")

def final_block(x_ini,y_ini,chanels_in,chanels_mid,chanels_out,size_ini):
    lay2 = x_ini + dist_layers(chanels_in,chanels_mid)
    lay3 = lay2 + dist_layers(chanels_mid,chanels_mid)
    lay4 = lay3 + dist_layers(chanels_mid,chanels_out)
    layer(x_ini,y_ini,chanels_in,size_ini,col_layer)
    arrow_horizontal(x_ini+chanels_in/2+space,y_ini,col_arh)
    layer(lay2,y_ini,chanels_mid,size_ini,col_layer)
    arrow_horizontal(lay2+chanels_mid/2+space,y_ini,col_arh)
    layer(lay3,y_ini,chanels_mid,size_ini,col_layer)
    arrow_horizontal(lay3+chanels_mid/2+space,y_ini,col_arh)
    layer(lay4,y_ini,chanels_out,size_ini,col_layer)
    write_label(x_ini,y_ini,chanels_in,size_ini,"right")
    write_label(lay2,y_ini,chanels_mid,size_ini,"right")
    write_label(lay3,y_ini,chanels_mid,size_ini,"right")
    write_label(lay4,y_ini,chanels_out,size_ini,"right")

def write_label(x_lay,y_lay,channels,size_lay,direction):
    fill(0)
    textSize(10)
    pushMatrix()
    if direction=="left":
        translate(x_lay-channels/2.,y_lay+size_lay/2.+2.*space)
        textAlign(RIGHT)
        rotate(3.5*PI/2.)
    elif direction=="right":
        translate(x_lay+channels/2.,y_lay+size_lay/2.+2.*space)
        textAlign(LEFT)
        rotate(-3.5*PI/2.)
    elif direction=="up":
        translate(x_lay-channels/2.,y_lay-size_lay/2.-space)
        textAlign(RIGHT)
        rotate(-3.5*PI/2.)
    #scale(1,1);
    if channels==2.:
        chan = 1
    else:
        chan = channels*64/10
    text(str(chan)+", ("+str(size_lay)+"x"+str(size_lay)+")",0,0)
    popMatrix()

def legend(x,y,x2,y2):
    rectMode(CORNER)
    noStroke()
    fill(128)
    rect(x+space/2.,y+space/2.,x2-x+space/2.,y2-y+space/2.)
    stroke(0)
    fill(255)
    rect(x,y,x2-x,y2-y)

    noStroke()
    distleg = 10*space
    lay_w, lay_h = 15, 30
    x_lab1 = x + 2*space
    x_tex1 = x_lab1 + arr_size + space
    x_lab2 = x_tex1 + textWidth("Unit layer") + distleg
    x_tex2 = x_lab2 + arh + space
    x_lab3 = x_tex2 + textWidth("Max-Pooling") + distleg
    x_tex3 = x_lab3 + arh + space
    x_lab4 = x_tex3 + textWidth("Deconvolution") + distleg
    x_tex4 = x_lab4 + distleg + space
    x_lab5 = x_tex4 + textWidth("Concatenation") + distleg
    x_tex5 = x_lab5 + lay_w/2 + space
    x_lab6 = x_tex5 + textWidth("Output layer") + distleg
    x_tex6 = x_lab6 + lay_w/2 + space
    ylab = y + (y2-y)/2

    
    arrow_horizontal(x_lab1,ylab,col_arh)
    arrow_vertical(x_lab2,ylab-arr_size/2,+1,col_arv_down)
    arrow_vertical(x_lab3,ylab+arr_size/2,-1,col_arv_up)
    long_arrow(x_lab4,ylab,x_lab4+distleg)
    layer(x_lab5,ylab,lay_w,lay_h,col_layer)
    layer(x_lab6,ylab,lay_w,lay_h,col_layconc)
    
    fill(0)
    textSize(15)
    textAlign(LEFT, CENTER)
    text("Unit layer",x_tex1,ylab)
    text("Max-Pooling",x_tex2,ylab)
    text("Deconvolution",x_tex3,ylab)
    text("Concatenation",x_tex4,ylab)
    text("Output layer",x_tex5,ylab)
    text("Concatenated layer",x_tex6,ylab)


# SETUP AND DRAWING

def setup():
    size(1000,700,P2D)
    pixelDensity(2);
    background(255)
    noStroke()
    global f
    f = createFont("Arial",30,True)
    
def draw():
    #print(mouseX,mouseY)
    global f
    textFont(f) #textFont(f,10)
    
    # Positions encoders
    x_1 = 60
    y_1 = 175
    x_2 = x_1 + dist_layers(1,chanels) + dist_layers(chanels,chanels)
    y_2 = y_1 + dist_vert(size_ini)
    x_3 = x_2 + dist_layers(chanels,chanels*2) + dist_layers(chanels*2,chanels*2)
    y_3 = y_2 + dist_vert(size_ini/2)
    # Positions encoders
    x_4 = x_3 + dist_layers(chanels*2,chanels*4) + dist_layers(chanels*4,chanels*4)
    y_4 = y_3 + dist_vert(size_ini/4)
    x_5 = x_4 + dist_layers(chanels*4,chanels*8) + dist_layers(chanels*8,chanels*4)
    y_5 = y_4 - dist_vert(size_ini/4)
    x_6 = x_5 + dist_layers(chanels*8,chanels*4) + dist_layers(chanels*4,chanels*2)
    y_6 = y_5 - dist_vert(size_ini/2)
    x_7 = x_6 + dist_layers(chanels*4,chanels*2) + dist_layers(chanels*2,chanels)
    y_7 = y_6 - dist_vert(size_ini)

    # Encoder
    contracting_block(x_1,y_1,2,chanels,size_ini)
    contracting_block(x_2,y_2,chanels,chanels*2,size_ini/2)
    contracting_block(x_3,y_3,chanels*2,chanels*4,size_ini/4)
    
    # Concatenations
    concat_block(x_2,y_1,x_7,chanels,chanels*2,size_ini)
    concat_block(x_3,y_2,x_6,chanels*2,chanels*4,size_ini/2)
    concat_block(x_4,y_3,x_5,chanels*4,chanels*8,size_ini/4) 
    
    # Decoder
    expanding_block(x_4,y_4,chanels*4,chanels*8,chanels*4,size_ini/8)
    expanding_block(x_5,y_5,chanels*8,chanels*4,chanels*2,size_ini/4)
    expanding_block(x_6,y_6,chanels*4,chanels*2,chanels,size_ini/2)
    final_block(x_7,y_7,chanels*2,chanels,2,size_ini)
    
    # Legend
    x1_leg, y1_leg = x_1, y_4+size_ini/2
    x_2_leg, y_2_leg = x_7+20*space, y1_leg+size_ini/4
    legend(x1_leg, y1_leg,x_2_leg, y_2_leg)

    saveFrame("diagram2D.png")
    noLoop()
    
