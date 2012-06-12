import javax.swing.JFrame;
import java.awt.Dimension;
import java.awt.Toolkit;
import com.sun.awt.AWTUtilities;
import java.awt.Graphics;
import java.awt.Color;
import java.io.InputStream;
import javax.swing.ImageIcon;
import java.awt.Image;
import javax.imageio.ImageIO;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.AlphaComposite;
import java.awt.Frame;

/*
 * intro screen with Twister logo
 * and loading status bar
 */
public class IntroScreen extends JFrame{
    private String text = ""; //text used to display initialization status on loading bar
    int width;
    private double percent = 0; //percent of status bar set by initialization methods

    /*
     * intro screen initialization
     */
    public IntroScreen(){
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        setBounds((int)(screenSize.getWidth()-640)/2,(int)(screenSize.getHeight()-480)/2,640,480);
        setUndecorated(true);
        try{if(AWTUtilities.isTranslucencySupported(AWTUtilities.Translucency.PERPIXEL_TRANSLUCENT))AWTUtilities.setWindowOpaque(this, false);
            else if(AWTUtilities.isTranslucencySupported(AWTUtilities.Translucency.TRANSLUCENT))AWTUtilities.setWindowOpacity(this, 0.7f);}
        catch(Exception e){e.printStackTrace();}}
    
    public void paint(Graphics g){
        Graphics2D g2d = (Graphics2D)g;
        g2d.setComposite(AlphaComposite.Clear);
        g2d.fillRect(0, 0, 640, 480);
        g2d.setComposite(AlphaComposite.SrcOver);
        g.setColor(Color.GRAY);
        g.fillRoundRect(10, 350, (int)(620*percent), 30, 15, 15);
        g.setColor(Color.BLACK);
        g.drawRoundRect(10, 350, 620, 30, 15, 15);
        g.setFont(new Font("TimesRoman", 0, 14));
        g.drawString(text, 30, 374);
        g.drawImage(Repository.background, 55, 10, null);}
    
    /*
     * text - the text to display on loading
     * bar
     */   
    public void setStatus(String text){
        this.text = text;}
        
    /*
     * add percent to ilustrate
     * on loading bar
     */
    public void addPercent(double percent){
        this.percent+=percent;}}