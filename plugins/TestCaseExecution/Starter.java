import com.twister.plugin.twisterinterface.TwisterPluginInterface;
import com.twister.plugin.twisterinterface.CommonInterface;
import com.twister.plugin.baseplugin.BasePlugin;
import java.util.ArrayList;
import java.util.Hashtable;
import com.twister.Item;
import org.w3c.dom.Document;
import java.applet.Applet;
import java.awt.Component;
import java.net.URL;

public class Starter implements TwisterPluginInterface{
    public CommonInterface maincomp;
    
    public void init(ArrayList<Item> suite, ArrayList<Item> suitetest,
            final Hashtable<String, String> variables,
            final Document pluginsConfig,Applet container) {
                RunnerRepository.starter = this;
                PermissionValidtor.init(variables.get("permissions"));
                RunnerRepository.user = variables.get("user");
                RunnerRepository.password = variables.get("password");
                RunnerRepository.host = variables.get("host");
                container.removeAll();
                container.revalidate();
                container.repaint();
                RunnerRepository.initialize("true","tsc-server",container);
                try{
                    container.getAppletContext().showDocument(new URL("javascript:resize()"));
                } catch (Exception e) {
                    System.err.println("Failed to call JavaScript function appletLoaded()");
                }
    }
    
    public String getFileName() {
        String filename = "runner.jar";
        return filename;
    }
    
    public String getDescription(String desc){
        return "";
    }
    
    public void terminate(){}
    
    public String getName(){
        String name = "runner";
        return name;
    }
    
    public Component getContent() {
        return RunnerRepository.window.mainpanel;
    }
    
    public void setInterface(CommonInterface arg0) {
        this.maincomp=arg0;
    }
    
    public void resizePlugin(int width, int height){
        System.out.println("Starter resizing");
        RunnerRepository.setSize(width, height);
    }
}