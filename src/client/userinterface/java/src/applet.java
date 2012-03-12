import java.applet.Applet; 
import java.awt.Graphics; 
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Toolkit;
import javax.swing.ImageIcon;
import javax.swing.JOptionPane;
import java.io.File;
import javax.imageio.ImageIO;
import java.io.InputStream;
import java.io.BufferedReader;
import java.io.StringWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.awt.image.BufferedImage;

public class applet extends Applet{ 
    private static final long serialVersionUID = 1L;
     
    public void init(){
        try{System.out.println("Current version: ");
            System.out.println("OS current temporary directory is : "+System.getProperty("java.io.tmpdir"));
            System.out.println("Getting tc.png from applet jar...");
            InputStream in = getClass().getResourceAsStream("Icons"+"/"+"tc.png");
            System.out.println("Saving tc.png in memory.....");
            Repository.tcicon = new ImageIcon(ImageIO.read(in)).getImage();
            if(Repository.tcicon !=null)System.out.println("tc.png succsesfully loaded.");
            else System.out.println("tc.png not loaded.");
            System.out.println("Getting background.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"background.png"); 
            System.out.println("Saving background.png in memory.....");
            Repository.background = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.background !=null)System.out.println("background.png succsesfully loaded.");
            else System.out.println("background.png not loaded.");
            System.out.println("Getting pending.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"pending.png"); 
            System.out.println("Saving pending.png in memory.....");
            Repository.pendingicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.pendingicon !=null)System.out.println("pending.png succsesfully loaded.");
            else System.out.println("pending.png not loaded.");            
            System.out.println("Getting device.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"device.png"); 
            System.out.println("Saving device.png in memory.....");
            Repository.deviceicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.deviceicon !=null)System.out.println("device.png succsesfully loaded.");
            else System.out.println("device.png not loaded.");            
            System.out.println("Getting module.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"module.png"); 
            System.out.println("Saving module.png in memory.....");
            Repository.moduleicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.moduleicon !=null)System.out.println("module.png succsesfully loaded.");
            else System.out.println("module.png not loaded.");
            System.out.println("Getting notexec.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"notexec.png"); 
            System.out.println("Saving notexec.png in memory.....");
            Repository.notexecicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.notexecicon !=null)System.out.println("notexec.png succsesfully loaded.");
            else System.out.println("notexec.png not loaded."); 
            System.out.println("Getting skip.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"skip.png"); 
            System.out.println("Saving skip.png in memory.....");
            Repository.skipicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.skipicon !=null)System.out.println("skip.png succsesfully loaded.");
            else System.out.println("skip.png not loaded."); 
            System.out.println("Getting stopped.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"stopped.png"); 
            System.out.println("Saving stoped.png in memory.....");
            Repository.stoppedicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.stoppedicon !=null)System.out.println("stopedicon.png succsesfully loaded.");
            else System.out.println("stopicon.png not loaded."); 
            System.out.println("Getting timeout.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"timeout.png"); 
            System.out.println("Saving timeout.png in memory.....");
            Repository.timeouticon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.timeouticon !=null)System.out.println("timeout.png succsesfully loaded.");
            else System.out.println("timeout.png not loaded.");
            System.out.println("Getting wait.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"waiting.png"); 
            System.out.println("Saving wait.png in memory.....");
            Repository.waiticon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.waiticon !=null)System.out.println("wait.png succsesfully loaded.");
            else System.out.println("waiting.png not loaded.");
            System.out.println("Getting working.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"working.png"); 
            System.out.println("Saving working.png in memory.....");
            Repository.workingicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.workingicon !=null)System.out.println("working.png succsesfully loaded.");
            else System.out.println("working.png not loaded.");
            System.out.println("Getting suita.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"suita.png"); 
            System.out.println("Saving suita.png in memory.....");
            Repository.suitaicon = new ImageIcon(ImageIO.read(in)).getImage();
            if(Repository.suitaicon !=null)System.out.println("suitaicon.png succsesfully loaded.");
            else System.out.println("suitaicon.png not loaded.");
            System.out.println("Getting prop.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"prop.png"); 
            System.out.println("Saving prop.png in memory.....");
            Repository.propicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.propicon !=null)System.out.println("propicon.png succsesfully loaded.");
            else System.out.println("propicon.png not loaded.");
            System.out.println("Getting fail.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"fail.png"); 
            System.out.println("Saving fail.png in memory.....");
            Repository.failicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.failicon !=null)System.out.println("failicon.png succsesfully loaded.");
            else System.out.println("failicon.png not loaded.");
            System.out.println("Getting pass.png from applet jar...");
            in = getClass().getResourceAsStream("Icons"+"/"+"pass.png");
            System.out.println("Saving pass.png in memory.....");
            Repository.passicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.passicon !=null)System.out.println("passicon.png succsesfully loaded.");
            else System.out.println("passicon.png not loaded.");
            System.out.println("Getting stop.png from applet jar...");
            in = Repository.class.getResourceAsStream("Icons"+"/"+"stop.png");
            System.out.println("Saving stop.png in memory.....");
            Repository.stopicon = new ImageIcon(ImageIO.read(in)).getImage(); 
            if(Repository.stopicon !=null)System.out.println("stopicon.png succsesfully loaded.");
            else System.out.println("stopicon.png not loaded.");
            System.out.println("Getting play.png from applet jar...");
            in = Repository.class.getResourceAsStream("Icons"+"/"+"play.png");
            System.out.println("Saving play.png in memory.....");
            Repository.playicon = new ImageIcon(ImageIO.read(in)).getImage();
            if(Repository.playicon !=null)System.out.println("playicon.png succsesfully loaded.");
            else System.out.println("playicon.png not loaded.");
            System.out.println("Getting pause.png from applet jar...");
            in = Repository.class.getResourceAsStream("Icons"+"/"+"pause.png");
            System.out.println("Saving pause.png in memory.....");
            Repository.pauseicon = new ImageIcon(ImageIO.read(in)).getImage();
            if(Repository.pauseicon !=null)System.out.println("pauseicon.png succsesfully loaded.");
            else System.out.println("pauseicon.png not loaded.");
            System.out.println("Getting port.png from applet jar...");
            in = Repository.class.getResourceAsStream("Icons"+"/"+"port.png");
            System.out.println("Saving port.png in memory.....");
            Repository.porticon = new ImageIcon(ImageIO.read(in)).getImage();
            if(Repository.porticon !=null)System.out.println("port.png succsesfully loaded.");
            else System.out.println("port.png not loaded.");}
        catch(Exception e){e.printStackTrace();}
        setLayout(null);
        System.out.println("Size is: "+getSize().getWidth()+" - "+getSize().getHeight());
        Repository.initialize(true, getCodeBase().getHost(),this);}
    
    public void setSize(int width, int height){
        super.setSize(width,height);
        if(height>672)height=672;
        Repository.f.p.setSize(width-20,height-20);
        
        Repository.f.p.p2.splitPane.setSize(width-52,height-120);
        Repository.f.p.p1.splitPane.setSize(width-52,height-120);
        Repository.f.p.setSize(width-28,height-40);
        Repository.f.p.p3.pane.setSize(width-42,height-82);
        Repository.f.p.p4.scroll.setSize(width-310,height-150);
        Repository.f.p.p4.main.setSize(width-300,height-130);
        
        validate();}
    
    public void stop(){
        System.out.println("stopping");}
        
    public void destroy(){
        System.out.println("destroying");
        System.exit(0);}
        
    public void start(){
        System.out.println("starting");}}