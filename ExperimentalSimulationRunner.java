
import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.event.*;
import java.util.ArrayList;
import java.awt.event.MouseAdapter;

public class ExperimentalSimulationRunner extends Canvas{
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
    double subdiv = 10;
    boolean fireballs = true;
    ArrayList<VerletObject> objects = new ArrayList<VerletObject>();
    ArrayList<Integer> collisionCount = new ArrayList<Integer>();
    ArrayList<Integer> radius = new ArrayList<Integer>();
    //Make a method that updates the contents of a 2d array of arraylists.
    ArrayList<Integer>[][] grid = (ArrayList<Integer>[][]) new ArrayList[(int)subdiv][(int)subdiv];
    boolean mousePressed;
    public static void main(String[] args){
        final boolean[] running = new boolean[]{true};

        Frame frame =  new Frame("Simulator");

        ExperimentalSimulationRunner runner = new ExperimentalSimulationRunner();
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
                runner.radius.add((int)(Math.random()*45+5)); 
                runner.fireballs = !runner.fireballs;
                runner.mousePressed = true;
            }
            public void mouseReleased(MouseEvent e){
                runner.mousePressed = false;
            }
        });
        runner.addMouseMotionListener(new MouseMotionAdapter(){
            @Override
            public void mouseDragged(MouseEvent e){
                //System.out.println("Mouse dragged");
                runner.gravitycX = e.getX();
                runner.gravitycY = e.getY();
                int x = e.getX();
                int y = e.getY();
                runner.objects.add(new VerletObject(x, y, new double[]{20, 0}));
                runner.collisionCount.add(0);
                runner.radius.add((int)(Math.random()*45+5));
                
                runner.mousePressed = true;
            }
        });
        frame.add(runner);
        int theta = 0;
        while (running[0]){
            for (int i = 0; i < 20; i++){
                runner.update(0.05);
            }

            // runner.objects.add(new VerletObject(10, 10, new double[]{45 - 90 * Math.random(), -0.1}));
            //if (runner.fireballs){
                //runner.objects.add(new VerletObject(500, 500, new double[]{45 - 90 * Math.random(), -0.1}));

                // runner.objects.add(new VerletObject(450, 600, new double[]{0, 4}));
                //runner.collisionCount.add(0);
                //runner.radius.add(25);}
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
        for (int i = 0; i < objects.size(); i++){
            objects.get(i).collided.clear();
        }
        applygravity();
        addCenterofGravity(gravitycX, gravitycY, 9);
        addCenterofGravity(gravitycX2, gravitycY2, 9);
        //addCenterofGravity(gravitycX3, gravitycY3, 4);
        applyDistanceConstraint();
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
    public void applyDistanceConstraint(){
        for (int i = 0; i < objects.size(); i++){
            VerletObject obj1 = objects.get(i);
            ArrayList<Integer> temp = obj1.getCollided();
            for (int j = 0; j < temp.size(); j++){
                VerletObject obj2 = objects.get(j);
                double to_objx = obj2.currposex - obj1.currposex;
                double to_objy = obj2.currposey - obj1.currposey;
                double distance = Math.sqrt(to_objx * to_objx + to_objy * to_objy);
                if (distance > 2*radius.get(i) - radius.get(j)-30){
                    double nx = to_objx / distance;
                    double ny = to_objy / distance;
                    objects.get(i).currposex = obj1.currposex + nx * (2*radius.get(i) - radius.get(j));
                    objects.get(i).currposey = obj1.currposey + ny * (2*radius.get(i) - radius.get(j));
                }

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
    public void solveCollisions(int i1, int i2) {
        VerletObject obj1 = objects.get(i1);
        VerletObject obj2 = objects.get(i2);
        double x1 = obj1.currposex;
        double y1 = obj1.currposey;
        double x2 = obj2.currposex;
        double y2 = obj2.currposey;
        double dist = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
        double overlap = radius.get(i1) + radius.get(i2) - dist;
    
        if (overlap > 0) {
            if (!objects.get(i1).collided.contains(i2)) {
                objects.get(i1).collided.add(i2);
            }
            if (!objects.get(i2).collided.contains(i1)) {
                objects.get(i2).collided.add(i1);
            }
            collisionCount.set(i1, collisionCount.get(i1) + 1);
            collisionCount.set(i2, collisionCount.get(i2) + 1);
    
            // Calculate the normalized direction vector
            double nx = (x2 - x1) / dist;
            double ny = (y2 - y1) / dist;
    
            // Adjust positions based on the overlap
            double adjustX = nx * overlap / 2;
            double adjustY = ny * overlap / 2;
    
            obj1.currposex -= adjustX;
            obj1.currposey -= adjustY;
            obj2.currposex += adjustX;
            obj2.currposey += adjustY;
    
            // Calculate the new velocities after collision
            double v1x = obj1.velocityx;
            double v1y = obj1.velocityy;
            double v2x = obj2.velocityx;
            double v2y = obj2.velocityy;
    
            // Calculate the dot product of velocity difference and normal vector
            double vDotN = (v2x - v1x) * nx + (v2y - v1y) * ny;
    
            if (vDotN > 0) {
                return; // They are separating, no need to adjust velocities
            }
    
            // Elastic collision response
            double restitution = 0.8; // Adjust this value for more or less bounciness
            double impulse = (1 + restitution) * vDotN / 2;
    
            obj1.velocityx -= impulse * nx;
            obj1.velocityy -= impulse * ny;
            obj2.velocityx += impulse * nx;
            obj2.velocityy += impulse * ny;
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
    public ExperimentalSimulationRunner(){
        offscreenImage = new BufferedImage(1000, 1000, BufferedImage.TYPE_INT_ARGB);
        offscreenGraphics = offscreenImage.createGraphics();
        setSize(new Dimension(1000, 1000));
        setBackground(Color.BLACK);
        createGridImage();
    }
    @Override
    public void paint(Graphics g) {
        super.paint(g);
        offscreenGraphics.setColor(getBackground());
        offscreenGraphics.fillRect(0, 0, getWidth(), getHeight());
        offscreenGraphics.drawImage(gridImage, 0, 0, null);
        int[] curr = new int[]{0, 0, 255};
        int[] goal = new int[]{0, 0, 127};

        for (int i = 0; i < objects.size(); i++) {
            double vx = objects.get(i).velocityx;
            double vy = objects.get(i).velocityy;
            double mag = Math.sqrt(vx * vx + vy * vy);
            double normalizedVelocity = Math.pow(Math.min(mag / 10, 1.0), 0.5);
            curr[0] = (int) (normalizedVelocity * 255 * 1.25);
            if (curr[0] > 255) {
                curr[0] = 255;
            }
            offscreenGraphics.setColor(new Color(curr[0], curr[1], curr[2]));
            int radiusValue = radius.get(i);
            int posX = (int) (objects.get(i).currposex - radiusValue);
            int posY = (int) (objects.get(i).currposey - radiusValue);

            //offscreenGraphics.fillOval(posX, posY, 2 * radiusValue, 2 * radiusValue);

            // Draw object information as text

            ArrayList<Integer> collided = objects.get(i).getCollided();
            for (int j = 0; j < collided.size(); j++) {
                int k = collided.get(j);
                offscreenGraphics.drawLine((int) (objects.get(i).currposex - radius.get(i)),
                                        (int) (objects.get(i).currposey - radius.get(i)),
                                        (int) (objects.get(k).currposex - radius.get(k)),
                                        (int) (objects.get(k).currposey - radius.get(k)));
            }
        }

        // Draw additional text (example: number of objects)
        offscreenGraphics.setColor(Color.WHITE);
        if (mousePressed){
            offscreenGraphics.drawString("Mouse pressed", 10, 20);
        }
        else{
            offscreenGraphics.drawString("Mouse let go", 10, 20);
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
        //g2d.drawLine(100, 600 , 900, 600);
        g2d.dispose();
    }
    
}
