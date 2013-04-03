import javax.swing.JPanel;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Font;

public class About extends JPanel{
    public About(){
        setLayout(new BorderLayout());
        JPanel p = new JPanel(){
            public void paint(Graphics g){
                //Graphics2D g2d = (Graphics2D)g;
                //g2d.setComposite(AlphaComposite.Clear);
                //g2d.fillRect(0, 0, 640, 480);
                //g2d.setComposite(AlphaComposite.SrcOver);
                //g.setColor(Color.GRAY);
                //g.fillRoundRect(10, 350, (int)(620*percent), 30, 15, 15);
                //g.setColor(Color.BLACK);
                //g.drawRoundRect(10, 350, 620, 30, 15, 15);
                //g.setFont(new Font("TimesRoman", 0, 14));
                //g.drawString(text, 30, 374);
                g.drawImage(Repository.background, 0, 0, null);
                g.setFont(new Font("TimesRoman", Font.BOLD, 14));
                g.drawString("Twister Framework", 225, 150);
                g.drawString("V.: "+Repository.getVersion(), 265, 165);
            }
        };
        p.setBackground(Color.RED);
        p.setSize(new Dimension(400,300));
        p.setPreferredSize(new Dimension(400,300));
        p.setMinimumSize(new Dimension(400,300));
        p.setMaximumSize(new Dimension(400,300));
        add(p,BorderLayout.CENTER );
    }

    
}
