import javax.swing.JFrame;
import java.io.InputStream;
import javax.swing.ImageIcon;
import javax.imageio.ImageIO;
import java.awt.Graphics;

public class MyMain{
    private static String bar = System.getProperty("file.separator");//System specific file.separator
    
    public static void main(String [] args){
        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setBounds(100,100,800,600);
        frame.setVisible(true);
        frame.setLayout(null);
        loadResourcesFromLocal();
        MainRepository.initialize(null,"tsc-server",frame.getContentPane());
    }
    
    /*
     * load resources needed for framework
     * from local pc
     */
    public static void loadResourcesFromLocal(){
        try{
            InputStream in;
            in = MainRepository.class.getResourceAsStream("Icons"+bar+"background.png"); 
            MainRepository.background = new ImageIcon(ImageIO.read(in)).getImage();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
