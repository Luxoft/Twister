import javax.swing.JPanel;
import java.awt.Color;

public class Panel5 extends JPanel{
    public NetTop nettop; 
    
    public Panel5(int width, int height){
        setBackground(Color.WHITE);
        setBounds(10,10,width,height);
        nettop = new NetTop(width,height);
        add(nettop);}}