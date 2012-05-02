import javax.swing.JPanel;
import javax.swing.JEditorPane;
import javax.swing.event.HyperlinkListener;
import java.net.URL;
import javax.swing.event.HyperlinkEvent;
import javax.swing.text.html.HTMLFrameHyperlinkEvent;

public class Browser{   
    public JEditorPane displayEditorPane; 
    
    public Browser(){
        displayEditorPane = new JEditorPane();
        displayEditorPane.setContentType("text/html");
        displayEditorPane.setEditable(false);
        try{displayEditorPane.setPage(new URL("http://"+Repository.host+":"+Repository.getHTTPServerPort()));}
        catch(Exception e){System.out.println("could not get "+Repository.host+":"+Repository.getHTTPServerPort());}
        displayEditorPane.addHyperlinkListener(new HyperlinkListener(){
            public void hyperlinkUpdate(HyperlinkEvent e){
                HyperlinkEvent.EventType eventType = e.getEventType();
                if (eventType == HyperlinkEvent.EventType.ACTIVATED) {
                    if (!(e instanceof HTMLFrameHyperlinkEvent)){
                        try{displayEditorPane.setPage(e.getURL());}
                        catch(Exception ex){System.out.println("Could not get to:"+e.getURL());}}}}});}}