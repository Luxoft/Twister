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
import java.awt.Image;

public class applet extends Applet{ 
    private static final long serialVersionUID = 1L;
     
    public void init(){
        try{System.out.println("Current version: ");
            System.out.println("OS current temporary directory is : "+System.getProperty("java.io.tmpdir"));
            Repository.tcicon = loadIcon("tc.png");
            System.out.println("Repository.tcicon "+Repository.tcicon.getHeight(this));
            Repository.background = loadIcon("background.png");
            Repository.pendingicon = loadIcon("pending.png");
            Repository.deviceicon = loadIcon("device.png");
            Repository.moduleicon = loadIcon("module.png");
            Repository.notexecicon = loadIcon("notexec.png");
            Repository.skipicon = loadIcon("skip.png");
            Repository.stoppedicon = loadIcon("stopped.png");
            Repository.timeouticon = loadIcon("timeout.png");
            Repository.waiticon = loadIcon("waiting.png");
            Repository.workingicon = loadIcon("working.png");
            Repository.suitaicon = loadIcon("suita.png");
            Repository.propicon = loadIcon("prop.png");
            Repository.failicon = loadIcon("fail.png");
            Repository.passicon = loadIcon("pass.png");
            Repository.stopicon = loadIcon("stop.png");
            Repository.playicon = loadIcon("play.png");
            Repository.pauseicon = loadIcon("pause.png");
            Repository.porticon = loadIcon("port.png");
            Repository.testbedicon = loadIcon("testbed.png");}
        catch(Exception e){e.printStackTrace();}
        setLayout(null);
        System.out.println("Size is: "+getSize().getWidth()+" - "+getSize().getHeight());
        Repository.initialize(true, getCodeBase().getHost(),this);}
        
    public Image loadIcon(String icon){
        Image image = null;
        try{System.out.println("Getting "+icon+" from applet jar...");
            InputStream in = getClass().getResourceAsStream("Icons"+"/"+icon);
            System.out.println("Saving "+icon+" in memory.....");
            image = new ImageIcon(ImageIO.read(in)).getImage();
            if(image !=null)System.out.println(icon+" succsesfully loaded.");
            else System.out.println(icon+" not loaded.");}
        catch(Exception e){
            System.out.println("There was a problem in loading "+icon+" on "+image.toString());
            e.printStackTrace();}
        return image;}
    
    public void setSize(int width, int height){
        super.setSize(width,height);
        Repository.frame.mainpanel.setSize(width-20,height-20);
        Repository.frame.mainpanel.p2.splitPane.setSize(width-52,height-120);
        Repository.frame.mainpanel.p1.splitPane.setSize(width-52,height-120);
        Repository.frame.mainpanel.setSize(width-28,height-40);
        Repository.frame.mainpanel.p4.scroll.setSize(width-310,height-150);
        Repository.frame.mainpanel.p4.main.setSize(width-300,height-130);
        Repository.frame.mainpanel.p4.dut.setPreferredSize(new Dimension(width-300,height-150));
        System.out.println("Resizing to: "+width+" - "+height);
        validate();}
    
    public void stop(){
        System.out.println("applet stopping");}
        
    public void destroy(){
        System.out.println("applet destroying");
        File file = new File(Repository.temp);
        if(file.exists()){
            if(Fereastra.deleteTemp(file))System.out.println(Repository.temp+" deleted successfull");
            else System.out.println("Could not delete: "+Repository.temp);}
        System.exit(0);}
        
    public void start(){
        System.out.println("applt starting");}}