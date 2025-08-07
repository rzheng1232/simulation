package JavaParticleCollisionSimulations;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.event.*;
import java.util.ArrayList;
import java.awt.event.MouseAdapter;

public class JavaSimulationRunnerOptimizedFinal extends Canvas{
    double gravityx = 0;
    double gravityy = 10;
    double gravity = 0.5;
    double cX = 500;
    double cY = 500;
    int gravitycX = 0;
    int gravitycY = 0;
    int gravitycX2 = 500;
    int gravitycY2 = 500;
    int gravitycX3 = 0;
    int gravitycY3 = 0;
    double cr = 350;
    double subdiv = 100;
    boolean fireballs = true;
    ArrayList<VerletObject> objects = new ArrayList<VerletObject>();
    ArrayList<Integer> collisionCount = new ArrayList<Integer>();
    ArrayList<Integer> radius = new ArrayList<Integer>();
    //Make a method that updates the contents of a 2d array of arraylists.
    ArrayList<Integer>[][] grid = (ArrayList<Integer>[][]) new ArrayList[(int)subdiv][(int)subdiv];

    public static void main(String[] args){
        final boolean[] running = new boolean[]{true};

        Frame frame =  new Frame("Simulator");

        JavaSimulationRunnerOptimizedFinal runner = new JavaSimulationRunnerOptimizedFinal();
        frame.setVisible(true);
        runner.setSize(new Dimension(1000, 1000));
        frame.setSize(new Dimension(1000, 1000));
        for (int i = 0; i < runner.subdiv; i++){
            for (int j = 0; j < runner.subdiv; j++){
                runner.grid[i][j] = new ArrayList<>();
            }
        }
        frame.addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent we){
                runner.updateGrid((double)frame.getWidth(), (double)frame.getHeight());
                // for (int i = 0; i < runner.subdiv; i++){
                //     for (int j = 0; j < runner.subdiv; j++){
                //         ArrayList<Integer> row = runner.grid[i][j];
                //         for (Integer item : row){
                //             System.out.println("Box " + i + ", " + j + " contains: " + item);
                //         }
                //     }
                // }
                running[0] = false;
                System.exit(0);
            }
        });
        runner.addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                int x = e.getX();
                int y = e.getY();
                
                runner.objects.add(new VerletObject(x, y, new double[]{20, 0}));
                runner.collisionCount.add(0);
                runner.radius.add(5);
                runner.fireballs = !runner.fireballs;

            }
        });
        runner.addMouseMotionListener(new MouseMotionAdapter(){
            @Override
            public void mouseDragged(MouseEvent e){
                //System.out.println("Mouse dragged");
                runner.gravitycX = e.getX();
                runner.gravitycY = e.getY();
                
                
            }
        });
        frame.add(runner);
        int theta = 0;
        while (running[0]){
            for (int i = 0; i < 20; i++){
                runner.update(0.05);
            }

            // runner.objects.add(new VerletObject(10, 10, new double[]{45 - 90 * Math.random(), -0.1}));
            if (runner.fireballs){
                runner.objects.add(new VerletObject(10, 10, new double[]{45 - 90 * Math.random(), -0.1}));

                // runner.objects.add(new VerletObject(450, 600, new double[]{0, 4}));
                runner.collisionCount.add(0);
                runner.radius.add(5);}
            theta++;
            runner.gravitycX = (int)( runner.cX + 100 * Math.sin(theta) );
            runner.gravitycY = (int) (runner.cY + 100 * Math.cos(theta) );
            runner.gravitycX2 =(int)( runner.cX + 100 * Math.cos(theta) );
            runner.gravitycY2 = (int) (runner.cY + 100 * Math.sin(theta) );
            runner.gravitycX3 =(int)( runner.gravitycX+ 25 * Math.cos(theta) );
            runner.gravitycY3 = (int) (runner.gravitycY+25* Math.sin(theta) );
            
            runner.repaint();
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }

    }
    public void update(double dt){
        applygravity();
        addCenterofGravity(gravitycX, gravitycY, 9);
        //addCenterofGravity(gravitycX2, gravitycY2, 9);
        addCenterofGravity(gravitycX3, gravitycY3, 4);
        applyConstraint();
        //applyLinearConstraint();
        checkCollisionsOptimized();
        updatePositions(dt);
        updateGrid(1000, 1000);

        
    }
    public void updatePositions(double dt){

        for (int i = 0; i < objects.size(); i++){
            objects.get(i).updatePose(dt);
            if (objects.get(i).currposex>1000 || objects.get(i).currposex<0||objects.get(i).currposey>1000 || objects.get(i).currposey<0){
                objects.remove(i);
                radius.remove(i);
                collisionCount.remove(i);
            }
        }
        
    }
    public void applygravity(){
        for (int i = 0; i < objects.size(); i++){
            objects.get(i).accelerate(gravityx, gravityy);
        }
    }
    
    public void addCenterofGravity(int cX, int cY, int magnitude){

        // Get a line between center of gravity and ball, apply acceleration on that line
        for (int i = 0; i < objects.size(); i++){
            double dx = objects.get(i).currposex - cX;
            double dy = objects.get(i).currposey - cY;
            double d = Math.sqrt(dx*dx + dy*dy);
            // if (50/(d) >= 1){
            //     magnitude = (int) (magnitude * 50/(d*d));
            // }

            //double r = dy/dx;
            objects.get(i).accelerationx -= dx* magnitude/d;
            //System.out.println(objects.get(i).accelerationx);
            objects.get(i).accelerationy -= dy*magnitude/d;
        }
    }
    public void applyConstraint(){
        for (int i = 0; i < objects.size(); i++){
            double to_objx = objects.get(i).currposex - cX;
            double to_objy = objects.get(i).currposey - cY;
            double distance = Math.sqrt(to_objx * to_objx + to_objy * to_objy);
            if (distance > cr - radius.get(i)-10){
                double nx = to_objx / distance;
                double ny = to_objy / distance;
                objects.get(i).currposex = cX + nx * (cr - radius.get(i)-10);
                objects.get(i).currposey = cY + ny * (cr - radius.get(i)-10);
            }
        }
    } 
    public void applyLinearConstraint(){
        for (int i = 0; i < objects.size(); i++){
            double to_objxr = 800 - objects.get(i).currposex ;
            double to_objxl = objects.get(i).currposex -200;
            double to_objy = objects.get(i).currposey - 600;
            // if (to_objxr>radius.get(i)-20 && to_objxl>radius.get(i)-20){
            //     if (to_objy > radius.get(i)-20){
            //         objects.get(i).currposey -= to_objy+10;
            //     }            
            // }
            if (to_objy > radius.get(i)-20){
                objects.get(i).currposey -= to_objy+10;
            }            
            if (to_objxr<radius.get(i)-20){
                objects.get(i).currposex -= 1;
            }
            if (to_objxl<radius.get(i)-20){
                objects.get(i).currposex += 1;
            }
        }
    }
    public void checkCollisions(){
        ArrayList<VerletObject> objectsCopy = new ArrayList<>(objects);
        for (int i = 0; i < objectsCopy.size(); i++){
            double x1 = objectsCopy.get(i).currposex;
            double y1 = objectsCopy.get(i).currposey;
            for (int j = i; j < objectsCopy.size(); j++){
                if (j == i){
                    continue;
                }
                solveCollisions(i, j);
            }
        }
    }
    public void checkCollisionsOptimized(){
        for (int i = 1; i < subdiv - 1; i++){
            for (int j = 1; j < subdiv-1; j++){
                ArrayList<Integer> currcell = grid[i][j];
                for (int dx = -1; dx <= 1; dx++){
                    for (int dy = -1; dy <= 1; dy++){
                        ArrayList<Integer> othercell = grid[i+dx][j+dy];
                        check_cell_collisions(currcell, othercell);
                    }
                }
            }
        }
    }
    public void check_cell_collisions(ArrayList<Integer> cell, ArrayList<Integer> cell1){
        for (int obji1 : cell){
            for (int obji2 : cell1){
                if (obji1 != obji2){

                    solveCollisions(obji1, obji2);
                }
            }
        }
    }
    public void solveCollisions(int i1, int i2){
        VerletObject obj1 = objects.get(i1);
        VerletObject obj2 = objects.get(i2);
        double x1 = obj1.currposex;
        double y1 = obj1.currposey;
        double x2 = obj2.currposex;
        double y2 = obj2.currposey; 
        double dist = Math.sqrt((x2-x1)*(x2-x1) + (y2 - y1)*(y2-y1));
        if (dist < radius.get(i1)+radius.get(i2)){
            collisionCount.set(i1, collisionCount.get(i1)+1);
            collisionCount.set(i2, collisionCount.get(i2)+1);
            double nx = Math.abs(x2-x1) / dist;
            double ny = Math.abs(y2-y1) / dist;
            double deltai = Math.pow(0.99, collisionCount.get(i1)) * (180 - dist) + dist;
            double deltaj = Math.pow(0.99, collisionCount.get(i2)) * (180 - dist) + dist;

            if (deltai > dist && deltaj > dist){
                if (objects.get(i2).currposex < objects.get(i1).currposex){
                    objects.get(i2).currposex -= 0.001*nx*deltaj;
                    objects.get(i1).currposex += 0.001*nx*deltai;
                }
                else{
                    objects.get(i2).currposex += 0.001*nx*deltaj;
                    objects.get(i1).currposex -= 0.001*nx*deltai;
                }
                if (objects.get(i2).currposey < objects.get(i1).currposey){
                    objects.get(i2).currposey -= 0.001*ny*deltaj;
                    objects.get(i1).currposey += 0.001*ny*deltai;
                }
                else{
                    objects.get(i2).currposey += 0.001*ny*deltaj;
                    objects.get(i1).currposey -= 0.001*ny*deltai;
                }
                
            }
            else{
                if (objects.get(i2).currposex < objects.get(i1).currposex){
                    objects.get(i2).currposex -= 0.001*nx*(180-dist);
                    objects.get(i1).currposex += 0.001*nx*(180-dist);
                }
                else{
                    objects.get(i2).currposex += 0.001*nx*(180-dist);
                    objects.get(i1).currposex -= 0.001*nx*(180-dist);
                }
                if (objects.get(i2).currposey < objects.get(i1).currposey){
                    objects.get(i2).currposey -= 0.001*ny*(180-dist);
                    objects.get(i1).currposey += 0.001*ny*(180-dist);
                }
                else{
                    objects.get(i2).currposey += 0.001*ny*(180-dist);
                    objects.get(i1).currposey -= 0.001*ny*(180-dist);
                }

            }
            
        }
    }
    public void updateGrid(double width, double height){
        for (int i = 0; i < subdiv; i++){
            for (int j = 0; j < subdiv; j++){
                grid[i][j] = new ArrayList<>();
            }
        }
        double boxw = width / subdiv;
        double boxh = height / subdiv;
        for (int i = 0; i < objects.size(); i++){
            double x = objects.get(i).currposex;
            double y = objects.get(i).currposey;
            int row = (int)(x / boxw);
            int col = (int)(y / boxh);
            grid[row][col].add(i);

        }
    }
    BufferedImage offscreenImage;
    Graphics2D offscreenGraphics;
    public JavaSimulationRunnerOptimizedFinal(){
        offscreenImage = new BufferedImage(1000, 1000, BufferedImage.TYPE_INT_ARGB);
        offscreenGraphics = offscreenImage.createGraphics();
        setSize(new Dimension(1000, 1000));
        setBackground(Color.BLACK);
        createGridImage();
    }
    @Override
    public void paint(Graphics g){
        offscreenGraphics.setColor(getBackground());
        offscreenGraphics.fillRect(0, 0, getWidth(), getHeight());
        offscreenGraphics.drawImage(gridImage, 0, 0, null);
        int[] curr = new int[]{0, 0, 255};
        int[] goal = new int[]{0, 0, 127};
        // offscreenGraphics.setColor(Color.WHITE);
        // offscreenGraphics.fillOval(gravitycX-5, gravitycY-5, 10, 10);
        // offscreenGraphics.setColor(Color.GREEN);
        // offscreenGraphics.fillOval(gravitycX2-5, gravitycY2-5, 10, 10);
        // offscreenGraphics.setColor(Color.BLUE);
        // offscreenGraphics.fillOval(gravitycX3-5, gravitycY3-5, 10, 10);

        // System.out.println("x: "+ gravitycX);
        // System.out.println("y: " + gravitycY);
        for (int i = 0; i < objects.size(); i++){
            // if (curr[0] < goal[0]){
            //     curr[0]++;
            // }
            // if (curr[0] > goal[0]){
            //     curr[0]--;
            // }
            // if (curr[1] < goal[1]){
                
            //     curr[1]++;
            // }
            // if (curr[1] > goal[1]){
            //     curr[1]--;
            // }
            // if (curr[2] < goal[2]){
                
            //     curr[2]++;
            // }
            // if (curr[2] > goal[2]){
            //     curr[2]--;
            // }
            // if (curr[2] == 127 ){
            //     goal = new int[]{127, 0, 0};
            // }
            // if (curr[0] == 127 ){
            //     goal = new int[]{0, 127, 0};
            // }
            // if (curr[1] == 127 ){
            //     goal = new int[]{0, 0, 127};
            // }
            double vx = objects.get(i).velocityx;
            double vy = objects.get(i).velocityy;
            double mag = Math.sqrt(vx*vx + vy*vy); 
            double normalizedVelocity = Math.pow(Math.min(mag / (10), 1.0), 0.5);
            curr[0] = (int) (normalizedVelocity*255*1.25);//(curr[0] + normalizedVelocity * (255 - curr[0]));
            //System.out.println(normalizedVelocity);
            if (curr[0] > 255){
                curr[0]= 255;
            }
            offscreenGraphics.setColor(new Color(curr[0], curr[1], curr[2]));
            offscreenGraphics.fillOval((int)(objects.get(i).currposex-radius.get(i)), (int)(objects.get(i).currposey-radius.get(i)), (int)(2*radius.get(i)), (int)(2*radius.get(i)));
            
        }
        g.drawImage(offscreenImage, 0, 0, null);
        
    }
    BufferedImage gridImage;
    public void createGridImage() {
        gridImage = new BufferedImage(1000, 1000, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2d = gridImage.createGraphics();
        g2d.setColor(Color.lightGray);
        g2d.drawOval(500 - 350, 500 - 350, 700, 700);
        
        // for (int i = 0; i < subdiv; i++) {
        //     g2d.drawLine((int)(i * 1000 / subdiv), 0, (int)(i * 1000 / subdiv), 1000);
        //     g2d.drawLine(0, (int)(i * 1000 / subdiv), 1000, (int)(i * 1000 / subdiv));
        // }
        g2d.drawLine(100, 600 , 900, 600);
        g2d.dispose();
    }
}
