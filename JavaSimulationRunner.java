
import java.awt.*;

import java.awt.event.*;
import java.util.ArrayList;
import java.awt.event.MouseAdapter;

public class JavaSimulationRunner extends Canvas{
    double gravityx = 0;
    double gravityy = 10;
    double gravity = 1;
    int x = 400;
    int y = 500;
    double r = 10;

    ArrayList<VerletObject> objects = new ArrayList<VerletObject>();
    ArrayList<Integer> collisionCount = new ArrayList<Integer>();
    public static void main(String[] args){
        final boolean[] running = new boolean[]{true};

        Frame frame =  new Frame("Simulator");

        JavaSimulationRunner runner = new JavaSimulationRunner();
        frame.setVisible(true);
        runner.setSize(new Dimension(1000, 1000));
        frame.setSize(new Dimension(1000, 1000));
        frame.addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent we){
                running[0] = false;
                System.exit(0);
            }
        });
        runner.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                int x = e.getX();
                int y = e.getY();
                
                runner.objects.add(new VerletObject(x, y, new double[]{0, 0}));
                runner.collisionCount.add(0);
                System.out.println("Mouse clicked at (" + x + ", " + y + ")");
            }
        });
        frame.add(runner);
        while (running[0]){
            for (int i = 0; i < 20; i++){
                runner.update(0.05);
            }
            
            runner.repaint();
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
           //System.out.println();
        }

    }
    public void update(double dt){
        applygravity();
        applyConstraint();
        checkCollisions();
        updatePositions(dt);


        
    }
    public void updatePositions(double dt){

        for (int i = 0; i < objects.size(); i++){
            objects.get(i).updatePose(dt);
            //System.out.println("positiony: " + objects[i].currposey);
        }
        
    }
    public void applygravity(){
        for (int i = 0; i < objects.size(); i++){
            objects.get(i).accelerate(gravityx, gravityy);
        }
    }
    public void applyConstraint(){
        double positionx = 500;
        double positiony = 500;
        double radius = 350;
        for (int i = 0; i < objects.size(); i++){
            double to_objx = objects.get(i).currposex - positionx;
            double to_objy = objects.get(i).currposey - positiony;
            double distance = Math.sqrt(to_objx * to_objx + to_objy * to_objy);
            if (distance > radius - r-10){
                double nx = to_objx / distance;
                double ny = to_objy / distance;
                objects.get(i).currposex = positionx + nx * (radius - r-10);
                objects.get(i).currposey = positiony + ny * (radius - r-10);
            }
        }
    } 
    public void checkCollisions(){
        for (int i = 0; i < objects.size(); i++){
            double x1 = objects.get(i).currposex;
            double y1 = objects.get(i).currposey;
            for (int j = i+1; j < objects.size(); j++){
                double x2 = objects.get(j).currposex;
                double y2 = objects.get(j).currposey;
                double dist = Math.sqrt((x2-x1)*(x2-x1) + (y2 - y1)*(y2-y1));
                if (dist < r*2){
                    collisionCount.set(i, collisionCount.get(i)+1);
                    collisionCount.set(j, collisionCount.get(j)+1);
                    double nx = Math.abs(x2-x1) / dist;
                    double ny = Math.abs(y2-y1) / dist;
                    double deltai = Math.pow(0.99, collisionCount.get(i)) * (180 - dist) + dist;
                    double deltaj = Math.pow(0.99, collisionCount.get(j)) * (180 - dist) + dist;

                    if (deltai > dist && deltaj > dist){
                        if (objects.get(j).currposex < objects.get(i).currposex){
                            objects.get(j).currposex -= 0.001*nx*deltaj;
                            objects.get(i).currposex += 0.001*nx*deltai;
                        }
                        else{
                            objects.get(j).currposex += 0.001*nx*deltaj;
                            objects.get(i).currposex -= 0.001*nx*deltai;
                        }
                        if (objects.get(j).currposey < objects.get(i).currposey){
                            objects.get(j).currposey -= 0.001*ny*deltaj;
                            objects.get(i).currposey += 0.001*ny*deltai;
                        }
                        else{
                            objects.get(j).currposey += 0.001*ny*deltaj;
                            objects.get(i).currposey -= 0.001*ny*deltai;
                        }
                        
                    }
                    else{
                        if (objects.get(j).currposex < objects.get(i).currposex){
                            objects.get(j).currposex -= 0.001*nx*(180-dist);
                            objects.get(i).currposex += 0.001*nx*(180-dist);
                        }
                        else{
                            objects.get(j).currposex += 0.001*nx*(180-dist);
                            objects.get(i).currposex -= 0.001*nx*(180-dist);
                        }
                        if (objects.get(j).currposey < objects.get(i).currposey){
                            objects.get(j).currposey -= 0.001*ny*(180-dist);
                            objects.get(i).currposey += 0.001*ny*(180-dist);
                        }
                        else{
                            objects.get(j).currposey += 0.001*ny*(180-dist);
                            objects.get(i).currposey -= 0.001*ny*(180-dist);
                        }

                    }
                    
                }
            }
        }
    }
    public JavaSimulationRunner(){
        setSize(new Dimension(1000, 1000));
        setBackground(Color.BLACK);
    }
    public void paint(Graphics g){
        //g.setColor(Color.lightGray);
        //g.fillOval(500 - 350, 500 -350, 700, 700);
        
        for (int i = 0; i < objects.size(); i++){
            if (i % 2 == 0){g.setColor(Color.white);}
            else{
                g.setColor(Color.ORANGE);
            }
            
            g.fillOval((int)(objects.get(i).currposex-r), (int)(objects.get(i).currposey-r), (int)(2*r), (int)(2*r));
            
        }
        
    }
}
