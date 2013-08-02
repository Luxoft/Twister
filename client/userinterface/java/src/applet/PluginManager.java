import com.twister.plugin.twisterinterface.CommonInterface;
import java.io.File;

public class PluginManager implements CommonInterface{
    
    public void loadComponent(String comp){
        if(comp.equals("reports")){
            MainRepository.loadReports();
        } else if(comp.equals("login")){
            MainRepository.applet.init();
        } else {
//             File f = MainRepository.getRemoteFile(comp+".jar");
//             MainRepository.loadPlugin(f, comp);
            File f = MainRepository.getRemoteFile(comp+".jar");
            MainRepository.loadPlugin(comp);
        }
    }
    
    public void downloadJar(String comp){
    }
}
