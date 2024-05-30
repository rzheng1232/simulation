import javax.swing.*;
import java.awt.*;
import java.awt.geom.Ellipse2D;

public class testing extends JPanel {
    private static final int WIDTH = 800;
    private static final int HEIGHT = 600;
    private static final int STAR_RADIUS = 10;
    private static final int ORBIT_RADIUS = 100;
    private static final int SPEED = 2;

    private double angle1 = 0;
    private double angle2 = Math.PI; // 180 degrees opposite

    public testing() {
        setPreferredSize(new Dimension(WIDTH, HEIGHT));
        Timer timer = new Timer(20, e -> {
            angle1 += SPEED * 0.01;
            angle2 += SPEED * 0.01;
            repaint();
        });
        timer.start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        int centerX = WIDTH / 2;
        int centerY = HEIGHT / 2;

        int star1X = (int) (centerX + ORBIT_RADIUS * Math.sin(angle1));
        int star1Y = (int) (centerY + ORBIT_RADIUS * Math.cos(angle1));

        int star2X = (int) (centerX + ORBIT_RADIUS * Math.sin(angle2));
        int star2Y = (int) (centerY + ORBIT_RADIUS * Math.cos(angle2));

        // Draw center of masses
        g2d.setColor(Color.RED);
        g2d.fill(new Ellipse2D.Double(centerX - 2, centerY - 2, 4, 4));

        // Draw stars
        g2d.setColor(Color.BLUE);
        g2d.fill(new Ellipse2D.Double(star1X - STAR_RADIUS, star1Y - STAR_RADIUS, 2 * STAR_RADIUS, 2 * STAR_RADIUS));

        g2d.setColor(Color.GREEN);
        g2d.fill(new Ellipse2D.Double(star2X - STAR_RADIUS, star2Y - STAR_RADIUS, 2 * STAR_RADIUS, 2 * STAR_RADIUS));
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Binary Star Simulation");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(new testing());
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}
