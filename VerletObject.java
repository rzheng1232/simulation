import java.math.*;
import java.awt.*;
import java.util.*;
public class VerletObject{
    double currposex;
    double currposey;
    double oldposex;
    double oldposey;
    double accelerationx;
    double accelerationy;
    double velocityx;
    double velocityy;
    double initvelocityx;
    double initvelocityy;
    ArrayList<Integer> collided;
    public VerletObject(double initx, double inity, double[] initialvelocity){
        currposex = initx;
        currposey = inity;
        oldposex = currposex;
        oldposey = currposey;
        accelerationx = 0;
        accelerationy = 0;
        double theta = initialvelocity[0];
        double initv = initialvelocity[1];
        initvelocityy = initv * Math.cos(theta * Math.PI / 180);
        initvelocityx = initv * Math.sin(theta * Math.PI / 180);
        currposex = currposex + initvelocityx + accelerationx * 0.05 * 0.05;
        currposey = currposey + initvelocityy + accelerationy * 0.05 * 0.05;
        collided = new ArrayList<Integer>();
    }
    public void updatePose(double dt){
        velocityx = currposex - oldposex;
        velocityy = currposey - oldposey;
        oldposex = currposex;
        oldposey = currposey;
        currposex = currposex + velocityx + accelerationx * dt * dt;
        accelerationx = 0;
        currposey = currposey + velocityy + accelerationy * dt * dt;
        accelerationy = 0;
    }
    public void accelerate(double accx, double accy){
        accelerationx += accx;
        accelerationy += accy;
    }
    public void addCollided(int index){
        collided.add(index);
    }
    public ArrayList<Integer> getCollided(){
        return collided;
    }
    public void resetCollided(){
        collided.clear();
    }
}