import javax.swing.JPanel;
import java.awt.Color;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.KeyListener;
import java.awt.event.KeyEvent;
import java.awt.Rectangle;
import java.awt.Graphics;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Arrays;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JTextField;
import javax.swing.JOptionPane;
import javax.swing.JFrame;
import javax.swing.JButton;
import javax.swing.JLabel;
import java.io.File;
import java.awt.Font;
import javax.swing.JTextField;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import javax.swing.JComboBox;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.SwingUtilities;
import java.awt.FontMetrics;
import java.awt.dnd.DropTarget;
import javax.swing.tree.TreeModel;
import javax.swing.tree.TreeNode;
import javax.swing.tree.TreePath;
import java.awt.Dimension;
import javax.swing.JFileChooser;
import java.awt.Component;
import javax.swing.filechooser.FileFilter;
import javax.swing.InputMap;
import javax.swing.ComponentInputMap;
import javax.swing.KeyStroke;
import javax.swing.ActionMap;
import javax.swing.plaf.ActionMapUIResource;
import javax.swing.Action;
import javax.swing.AbstractAction;
import javax.swing.JComponent;
import java.util.Set;
import java.util.HashSet;
import java.awt.Cursor;
import java.awt.dnd.DragSource;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.Collections;
import java.awt.event.WindowFocusListener;
import java.awt.event.WindowEvent;
import java.awt.DefaultKeyboardFocusManager;
import java.util.Comparator;
import java.awt.event.InputEvent;
import java.awt.event.MouseMotionAdapter;

public class Grafic extends JPanel{
    private static final long serialVersionUID = 1L;
    private ArrayList <Integer> selected;
    private ArrayList <int []> selectedcolection = new ArrayList<int []>();
    private byte keypress;
    private JPopupMenu p = new JPopupMenu();
    private boolean foundfirstitem;
    private int y = 5;
    private String user;
    private boolean dragging=false;
    private ArrayList<Item>clone = new ArrayList<Item>();
    private int dragammount = 0;
    private boolean clearedSelection = false;
    private boolean dragscroll = true;
    private boolean scrolldown = false;
    private boolean scrollup = false;
    private int[] line = {-1,-1,-1,-1,-1};
    private boolean canrequestfocus = true;
    
    public Grafic(TreeDropTargetListener tdtl, String user){
        this.user=user;
        setFocusable(true);
        if(!user.equals("")){Repository.f.p.setTitleAt(0,(user.split("\\\\")[user.split("\\\\").length-1]).split("\\.")[0]);}
        add(p);
        DropTarget dropTarget = new DropTarget(this, tdtl);
        new Thread(){
            public void run(){
                while(Repository.run){
                    if(scrolldown){
                        int scrollvalue = Repository.f.p.p1.sc.pane.getVerticalScrollBar().getValue();
                        Repository.f.p.p1.sc.pane.getVerticalScrollBar().setValue(scrollvalue-10);}
                    else if(scrollup){
                        int scrollvalue = Repository.f.p.p1.sc.pane.getVerticalScrollBar().getValue();
                        Repository.f.p.p1.sc.pane.getVerticalScrollBar().setValue(scrollvalue+10);}
                    try{Thread.sleep(60);}
                    catch(Exception e){e.printStackTrace();}}}}.start();
        addMouseMotionListener(new MouseMotionAdapter(){
            public void mouseDragged(MouseEvent ev){
                if((ev.getModifiers() & InputEvent.BUTTON1_MASK) != 0){
                    if(dragging){handleDraggingLine(ev.getX(),ev.getY());}
                    else{//first time
                        if(dragammount<1)dragammount++;
                        else{
                            dragammount=0;
                            getClickedItem(ev.getX(),ev.getY());
                            if(selected.size()>0){
                                if(getItem(selected,false).getType()!=0){
                                    setCursor(DragSource.DefaultCopyDrop);
                                    if(!getItem(selected,false).isSelected()){
                                        deselectAll();
                                        int [] temporary = new int[selected.size()];
                                        for(int m=0;m<temporary.length;m++)temporary[m]=selected.get(m).intValue();
                                        selectedcolection.add(temporary);}
                                    ArrayList <Integer> temp = new ArrayList <Integer>();
                                    for(int i=selectedcolection.size()-1;i>=0;i--){
                                        for(int j=0;j<selectedcolection.get(i).length;j++){temp.add(new Integer(selectedcolection.get(i)[j]));}
                                        Item theone2 = getItem(temp,false).clone();  
                                        if(theone2.getType()==0){
                                            getItem(temp,false).select(false);
                                            selectedcolection.remove(i);
                                            temp.clear();
                                            continue;}
                                        clone.add(theone2);
                                        temp.clear();}                                
                                    removeSelected();
                                    dragging = true;}
                                ArrayList<Item> unnecessary = new ArrayList<Item>();                        
                                for(int i=0;i<clone.size();i++){
                                    Item one = clone.get(i);
                                    ArrayList<Integer>pos = (ArrayList<Integer>)one.getPos().clone();
                                    while(pos.size()>1){
                                        pos.remove(pos.size()-1);
                                        boolean found = false;
                                        for(int j=0;j<clone.size();j++){
                                            Item one2 = clone.get(j);
                                            ArrayList<Integer>pos2 = (ArrayList<Integer>)one2.getPos().clone();
                                            if(compareArrays(pos,pos2)){
                                                unnecessary.add(clone.get(i));
                                                found = true;
                                                break;}}
                                        if(found)break;}}
                                for(int i=0;i<unnecessary.size();i++){clone.remove(unnecessary.get(i));}}}}}}});
        addMouseListener(new MouseAdapter(){
            public void mousePressed(MouseEvent ev){}
            public void mouseEntered(MouseEvent ev){
                if(canrequestfocus)requestFocus();
                dragscroll = true;}
            public void mouseExited(MouseEvent ev){
                dragscroll = false;
                keypress = 0;}
            public void mouseReleased(MouseEvent ev){
                clearDraggingLine();
                scrolldown = false;
                scrollup = false; 
                Repository.f.p.p1.suitaDetails.clearDefs();
                Repository.f.p.p1.suitaDetails.setParent(null);
                dragammount=0;
                if(dragging){handleMouseDroped(ev.getY());}
                else handleClick(ev);}});
        addKeyListener(new KeyListener(){
            public void keyPressed(KeyEvent ev){
                if(ev.getKeyCode()==KeyEvent.VK_SHIFT){keypress=1;}
                if(ev.getKeyCode()==KeyEvent.VK_CONTROL){keypress=2;}
                if(ev.getKeyCode()==KeyEvent.VK_DELETE){removeSelected();}
                if(ev.getKeyCode()==KeyEvent.VK_UP){
                    ArrayList <Integer> temp = new ArrayList <Integer>();  
                    int last = selectedcolection.size()-1;
                    for(int j=0;j<selectedcolection.get(last).length;j++){temp.add(new Integer(selectedcolection.get(last)[j]));}
                    Item next = prevInLine(getItem(temp,false));
                    if(next!=null&&keypress!=2){
                        if(keypress!=1){
                            deselectAll();
                            selectItem(next.getPos());
                            if(next.getType()==2&&next.getPos().size()==1){
                                int userDefNr = next.getUserDefNr();
                                Repository.f.p.p1.suitaDetails.setParent(next);
                                if(userDefNr!=Repository.f.p.p1.suitaDetails.getDefsNr())System.out.println("Warning, suite "+next.getName()+" has "+userDefNr+" fields while in bd.xml are defined "+Repository.f.p.p1.suitaDetails.getDefsNr()+" fields");
                                try{for(int i=0;i<userDefNr;i++){Repository.f.p.p1.suitaDetails.getDefPanel(i).setDecription(next.getUserDef(i)[1]);}}
                                catch(Exception e){e.printStackTrace();}}
                            else{
                                Repository.f.p.p1.suitaDetails.clearDefs();
                                Repository.f.p.p1.suitaDetails.setParent(null);}}
                        else{
                            if(!clearedSelection){
                                deselectAll();
                                clearedSelection = true;
                                selectItem(getItem(temp,false).getPos());}
                            if(next.isSelected()){                            
                                int [] itemselected = selectedcolection.get(selectedcolection.size()-1);
                                Item theone = Repository.getSuita(itemselected[0]);
                                for(int j=1;j<itemselected.length;j++){theone = theone.getSubItem(itemselected[j]);}
                                theone.select(false);
                                selectedcolection.remove(selectedcolection.size()-1);}
                            else selectItem(next.getPos());}
                        repaint();}}
                if(ev.getKeyCode()==KeyEvent.VK_DOWN){
                    ArrayList <Integer> temp = new ArrayList <Integer>();  
                    int last = selectedcolection.size()-1;
                    for(int j=0;j<selectedcolection.get(last).length;j++){temp.add(new Integer(selectedcolection.get(last)[j]));}
                    Item next = nextInLine(getItem(temp,false));
                    if(next!=null&&keypress!=2){
                        if(keypress!=1){
                            deselectAll();
                            selectItem(next.getPos());
                            if(next.getType()==2&&next.getPos().size()==1){
                                int userDefNr = next.getUserDefNr();
                                Repository.f.p.p1.suitaDetails.setParent(next);
                                if(userDefNr!=Repository.f.p.p1.suitaDetails.getDefsNr())System.out.println("Warning, suite "+next.getName()+" has "+userDefNr+" fields while in bd.xml are defined "+Repository.f.p.p1.suitaDetails.getDefsNr()+" fields");
                                try{for(int i=0;i<userDefNr;i++){Repository.f.p.p1.suitaDetails.getDefPanel(i).setDecription(next.getUserDef(i)[1]);}}
                                catch(Exception e){e.printStackTrace();}}
                            else{
                                Repository.f.p.p1.suitaDetails.clearDefs();
                                Repository.f.p.p1.suitaDetails.setParent(null);}}
                        else{
                            if(!clearedSelection){
                                deselectAll();
                                clearedSelection = true;
                                selectItem(getItem(temp,false).getPos());}
                            if(next.isSelected()){                            
                                int [] itemselected = selectedcolection.get(selectedcolection.size()-1);
                                Item theone = Repository.getSuita(itemselected[0]);
                                for(int j=1;j<itemselected.length;j++){theone = theone.getSubItem(itemselected[j]);}
                                theone.select(false);
                                selectedcolection.remove(selectedcolection.size()-1);}
                            else selectItem(next.getPos());}
                        repaint();}}}
            public void keyReleased(KeyEvent ev){
                if(ev.getKeyCode()!=KeyEvent.VK_UP&&ev.getKeyCode()!=KeyEvent.VK_DOWN){
                    if(ev.getKeyCode()!=KeyEvent.VK_SHIFT)clearedSelection=false;
                    keypress=0;}}
            public void keyTyped(KeyEvent ev){}});}
            
    public void clearDraggingLine(){
        line[0] = -1;
        line[1] = line[0];
        line[2] = line[0];
        line[3] = line[0];
        line[4] = line[0];}
            
    public void handleMouseDroped(int mouseY){
        Collections.sort(clone, new CompareItems());
        dragging=false;
        setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
        int Xpos = 0;
        while(Xpos<getWidth()){
            getClickedItem(Xpos,mouseY);
            Xpos+=5;
            if(selected.size()!=0)break;}
        if(selected.size()==0){
            int y1 = mouseY;
            Item upper=null;
            while(y1>0){
                y1-=5;
                for(int x1=0;x1<getWidth();x1+=5){
                    getClickedItem(x1,y1);
                    if(selected.size()>0){
                        upper=getItem(selected,false);
                        if(upper!=null)break;}
                    if(upper!=null)break;}}
            if(upper!=null){
                if(upper.getType()==1){//bagat sub tc
                    int index = upper.getPos().get(upper.getPos().size()-1).intValue();
                    int position = upper.getPos().size()-1;
                    ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone();
                    if(temp.size()>1)temp.remove(temp.size()-1);
                    Item parent = getItem(temp,false);                                
                    if(parent.getType()==1){dropOnFirstLevel(upper);}  //daca parintele upperului e de tipul tc inseamna ca e pe nivelul 0 si nu va avea parinte
                    else{ // parintele nu e un tc atunci nu e pe nivelul 0 si trebuie adaugat la parinte  sau dupa parinte  
                        if((parent.getSubItemsNr()-1==upper.getPos().get(upper.getPos().size()-1)) && !upper.getSubItem(0).isVisible()){//daca tc-ul e ultimul din suita                                     
                            int Y = mouseY;
                            if(Y<upper.getRectangle().y+upper.getRectangle().getHeight()+5){dropNextInLine(upper,parent,index,position);}//Should be inserted in upper parent/next in line; 5 e jumatate din distante dintre elemente
                            else{//Should be inserted after upper parent; exit one level
                                upper = parent;
                                position = upper.getPos().size();                                
                                int temp1 = upper.getPos().get(position-1);
                                if(upper.getPos().size()==1){dropOnFirstLevel(upper);}//Suita din repo pe nivelul 0
                                else{dropOnUpperLevel(upper);}}}  //Suita cu parent suita                                        
                        else{dropNextInLine(upper, parent, index, position);}}}//tc-ul nu este ultimul din suita si se face drop dupa el
                else if(upper.getType()==2){//bagat sub o suita
                    int Y = mouseY;
                    if((upper.getSubItemsNr()>0&&upper.getSubItem(0).isVisible())){//suita este expanded sau nu are copii si trebuie bagat in ea
                        dropFirstInSuita(upper);}//Should be inserted in suita
                    else if(Y<upper.getRectangle().y+upper.getRectangle().getHeight()+5){
                        int position = upper.getPos().size();                                
                        int temp1 = upper.getPos().get(position-1);
                        if(upper.getPos().size()==1){dropOnFirstLevel(upper);}//Suita din repo pe nivelul 0
                        else{int index = upper.getPos().get(upper.getPos().size()-1).intValue();
                            position = upper.getPos().size()-1;
                            ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone();
                            if(temp.size()>1)temp.remove(temp.size()-1);
                            Item parent = getItem(temp,false);                                        
                            dropNextInLine(upper, parent, index, position);}}
                    else{//suita nu este expanded sau nu are copii si nu sa facut drop aproape de ea , Should be inserted after suita
                        upper = upper.getFirstSuitaParent(false);                                    
                        if(upper.getPos().size()>1) dropOnUpperLevel(upper);
                        else dropOnFirstLevel(upper);}}//Suita cu parent suita
                else if(upper.getType()==0){
                    int Y = mouseY;//se face ca upper sa devina parentul acestui prop si se copiaza metodele de la drop sub tc, se face ca 
                    Y-=upper.getRectangle().y+upper.getRectangle().getHeight();
                    ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone();
                    temp.remove(temp.size()-1);
                    Item prop = upper;
                    upper = getItem(temp,false);
                    Y+=upper.getRectangle().y+upper.getRectangle().getHeight();                                
                    int index = upper.getPos().get(upper.getPos().size()-1).intValue();
                    int position = upper.getPos().size()-1;
                    temp = (ArrayList<Integer>)upper.getPos().clone();
                    if(temp.size()>1)temp.remove(temp.size()-1);
                    Item parent = getItem(temp,false);                                
                    if(parent.getType()==1){dropOnFirstLevel(upper);}  //daca parintele e de tipul tc inseamna ca e pe nivelul 0 si nu va avea parinte
                    else{ // parintele nu e un tc atunci nu e pe nivelul 0 si trebuie adaugat la parinte  sau dupa parinte  
                        if(prop.getTcParent(false).getSubItemsNr()-1==prop.getPos().get(prop.getPos().size()-1) && parent.getSubItemsNr()-1==upper.getPos().get(upper.getPos().size()-1)){//daca prop e ultimul din tc si tc-ul e ultimul din suita                                     
                            if(Y<upper.getRectangle().y+upper.getRectangle().getHeight()+5){dropNextInLine(upper, parent, index, position);}//5 e jumatate din distante dintre elemente, Should be inserted in upper parent
                            else{//Should be inserted after upper parent
                                upper = parent;
                                position = upper.getPos().size();                                
                                int temp1 = upper.getPos().get(position-1);
                                if(upper.getPos().size()==1){dropOnFirstLevel(upper);}//suita din repo pe nivelul 0
                                else{dropOnUpperLevel(upper);}}}//Suita cu parent suita
                        else{dropNextInLine(upper, parent, index, position);}}}}//tc-ul nu este ultimul din suita
            else{dropFirstElement();}}//upper is null
        else{
            if(getItem(selected,false).getType()==2){dropFirstInSuita(getItem(selected,false));}//bagat in suita                            
            else if(getItem(selected,false).getType()==1){//bagat in tc
                Item item = getItem(selected,false);
                boolean up = isUpperHalf(item, mouseY);
                if(up){//System.out.println("deasupra tc");
                    Item upper = item; //tc elementul in care sa facut drop
                    int index = upper.getPos().get(upper.getPos().size()-1).intValue(); //valoare ultimei pozitie al tc
                    int position = upper.getPos().size()-1; //al catelea elem e cel din care s-a facut drop
                    ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone(); //clona a pozitiei elemetului la care s-a facut drop
                    if(temp.size()>1)temp.remove(temp.size()-1); //se sterge ultima pozitie pentru a lua parentul
                    Item parent = getItem(temp,false); //parentul celui de deasupta
                    if(parent.getType()==2){dropPreviousInLine(upper,parent,index,position);}
                    else{
                        if(upper.getPos().get(0)>0){//trebuie adaugat inaintea upperului, nu va fi primul element
                            temp = (ArrayList<Integer>)upper.getPos().clone(); //clona a pozitiei elemetului la care s-a facut drop
                            temp.set(0,temp.get(0)-1);//se ia cel dinaintea lui
                            upper = getItem(temp,false); 
                            dropOnFirstLevel(upper);}
                        else{dropFirstElement();}}}//va fi primul element
                else{Item upper = item;//sub tc
                    int index = upper.getPos().get(upper.getPos().size()-1).intValue();
                    int position = upper.getPos().size()-1;
                    ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone();
                    if(temp.size()>1)temp.remove(temp.size()-1);
                    Item parent = getItem(temp,false);
                    if(parent.getType()==1)dropOnFirstLevel(upper);//parintele e de tipul tc>e pe nivelul 0
                    else dropNextInLine(upper, parent, index, position);}}//parintele nu e de tipul tc>se poate adauga in continuare sub parinte
            else if(getItem(selected,false).getType()==0){//bagat in prop
                ArrayList<Integer> temp = (ArrayList<Integer>)getItem(selected,false).getPos().clone();
                temp.remove(temp.size()-1);                            
                Item upper = getItem(temp,false);
                int index = upper.getPos().get(upper.getPos().size()-1).intValue();
                int position = upper.getPos().size()-1;
                temp = (ArrayList<Integer>)upper.getPos().clone();
                if(temp.size()>1)temp.remove(temp.size()-1);
                Item parent = getItem(temp,false);
                if(parent.getType()==1)dropOnFirstLevel(upper);//parintele e de tipul tc>e pe nivelul 0
                else dropNextInLine(upper, parent, index, position);}}}
            
    public boolean isUpperHalf(Item item, int Y){
        int middle = item.getLocation()[1]+(int)item.getRectangle().getHeight()/2;
        if(Y<=middle)return true;
        return false;}
            
    public void dropFirstElement(){
        int temp1 = 0;
        y=10;
        foundfirstitem=true;
        for(int i=0;i<clone.size();i++){
           ArrayList<Integer> selected2 = new ArrayList<Integer>();
           selected2.add(new Integer(i));
           clone.get(i).setPos(selected2);                               
           for(int j = temp1;j<Repository.getSuiteNr();j++){
                Repository.getSuita(j).updatePos(0,new Integer(Repository.getSuita(j).getPos().get(0).intValue()+1));}
           temp1++;
           clone.get(i).select(false);
           Repository.getSuite().add(clone.get(i).getPos().get(0), clone.get(i));}
        deselectAll();
        clone.clear();
        updateLocations(Repository.getSuita(0));
        repaint();}
            
    public void dropOnFirstLevel(Item upper){
        int position = upper.getPos().size();                                
        int temp1 = upper.getPos().get(position-1);                                    
        for(int i=0;i<clone.size();i++){
           ArrayList<Integer> selected2 = (ArrayList<Integer>)upper.getPos().clone();
           selected2.set(0,new Integer(upper.getPos().get(0)+i+1));
           clone.get(i).setPos(selected2);
           for(int j = temp1+1;j<Repository.getSuiteNr();j++){
                Repository.getSuita(j).updatePos(0,new Integer(Repository.getSuita(j).getPos().get(0).intValue()+1));}
           temp1++;
           clone.get(i).select(false);
           Repository.getSuite().add(clone.get(i).getPos().get(0), clone.get(i));}
        deselectAll();
        clone.clear();
        updateLocations(Repository.getSuita(0));
        repaint();}
        
    public void dropNextInLine(Item upper,Item parent,int index,int position){
        int temp1 = index+1;
        for(int i=0;i<clone.size();i++){
            ArrayList<Integer> selected2 = (ArrayList<Integer>)upper.getPos().clone();
            selected2.set(selected2.size()-1,new Integer(selected2.get(selected2.size()-1).intValue()+(i+1)));
            clone.get(i).setPos(selected2);
            for(int j = temp1;j<parent.getSubItemsNr();j++){
                parent.getSubItem(j).updatePos(position,new Integer(parent.getSubItem(j).getPos().get(position).intValue()+1));}
            temp1++;
            insertNewTC(clone.get(i).getName(),selected2,parent,clone.get(i));}    
        deselectAll();
        clone.clear();}   
        
    public void dropPreviousInLine(Item upper, Item parent, int index, int position){
        int temp1 = index;  //valoare ultimei pozitie al tc
        ArrayList<Integer> selected2 = (ArrayList<Integer>)upper.getPos().clone();
        for(int i=0;i<clone.size();i++){//se iau toate eleme din drag
            ArrayList<Integer> selected3 = (ArrayList<Integer>)selected2.clone(); //clona la pozitia elementul in care s-a facut drop
            selected3.set(selected3.size()-1,new Integer(selected3.get(selected3.size()-1).intValue()+i)); // 
            clone.get(i).setPos(selected3);
            for(int j = temp1;j<parent.getSubItemsNr();j++){
                parent.getSubItem(j).updatePos(position,new Integer(parent.getSubItem(j).getPos().get(position).intValue()+1));}
            temp1++;
            insertNewTC(clone.get(i).getName(),selected3,parent,clone.get(i));}    
        deselectAll();
        clone.clear();}
        
    public void dropOnUpperLevel(Item upper){
        int index = upper.getPos().get(upper.getPos().size()-1).intValue();
        int position = upper.getPos().size()-1;
        ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone();
        if(temp.size()>1)temp.remove(temp.size()-1);
        Item parent = getItem(temp,false);
        int temp1 = index+1;
        for(int i=0;i<clone.size();i++){
            ArrayList<Integer> selected2 = (ArrayList<Integer>)upper.getPos().clone();
            selected2.set(selected2.size()-1,new Integer(selected2.get(selected2.size()-1).intValue()+(i+1)));
            clone.get(i).setPos(selected2);
            for(int j = temp1;j<parent.getSubItemsNr();j++){
                parent.getSubItem(j).updatePos(position,new Integer(parent.getSubItem(j).getPos().get(position).intValue()+1));}
            temp1++;
            insertNewTC(clone.get(i).getName(),selected2,parent,clone.get(i));}    
        deselectAll();
        clone.clear();}
        
    public void dropFirstInSuita(Item upper){
        int position = upper.getPos().size();
        Item parent = upper;
        int temp1 = 0;
        for(int i=0;i<clone.size();i++){
            ArrayList<Integer> selected2 = (ArrayList<Integer>)upper.getPos().clone();
            selected2.add(new Integer(i));
            clone.get(i).setPos(selected2);
            for(int j = temp1;j<parent.getSubItemsNr();j++){
                parent.getSubItem(j).updatePos(position,new Integer(parent.getSubItem(j).getPos().get(position).intValue()+1));}
            temp1++;
            insertNewTC(clone.get(i).getName(),selected2,parent,clone.get(i));}    
        deselectAll();
        clone.clear();}
            
    public void lineInsideSuita(Item item, int X){
        line[0] = (int)(item.getRectangle().x+item.getRectangle().getWidth()/2-55);
        line[1] = (int)(item.getRectangle().y+item.getRectangle().getHeight()+5);
        line[2] = X;
        line[3] = line[1];
        line[4] = (int)(item.getRectangle().y+item.getRectangle().getHeight()+5);}
        
    public void lineOnSuita(Item item, int X){
        line[0] = (int)(item.getRectangle().x+item.getRectangle().getWidth()-40);
        line[1] = (int)(item.getRectangle().y+item.getRectangle().getHeight()/2);
        line[2] = X;
        line[3] = line[1];
        line[4] = line[3];}
        
    public void lineUnderSuita(Item item,int X){
        line[0] = (int)(item.getRectangle().x-25);
        line[1] = (int)(item.getRectangle().y+item.getRectangle().getHeight()+5);
        line[2] = X;
        line[3] = line[1];
        if(item.getFirstSuitaParent(false)!=null)line[4] = (int)(item.getFirstSuitaParent(false).getRectangle().y+item.getFirstSuitaParent(false).getRectangle().getHeight()+5);
        else line[4] = line[2];}
        
    public void lineAboveTc(Item item, int X){
        line[0] = (int)(item.getRectangle().x-25);
        line[1] = (int)(item.getRectangle().y-5);
        line[2] = X;
        line[3] = line[1];
        line[4] = line[1];}
        
    public void lineUnderTc(Item item, int X){
        line[0] = (int)(item.getRectangle().x-25);
        line[2] = X;
        if(item.getSubItem(0).isVisible()){line[1] = (int)(item.getSubItem(item.getSubItemsNr()-1).getRectangle().y+item.getSubItem(item.getSubItemsNr()-1).getRectangle().getHeight()+5);}
        else{line[1] = (int)(item.getRectangle().y+item.getRectangle().getHeight()+5);}
        line[3] = line[1];
        line[4] = (int)(item.getRectangle().y+item.getRectangle().getHeight()/2);}
        
    public void lineAfterUpperParent(Item item, int X){
        line[0] = (int)(item.getFirstSuitaParent(false).getRectangle().x-25);
        line[2] = X;
        if(item.getSubItemsNr()>0&&item.getSubItem(0).isVisible()){line[1] = (int)(item.getSubItem(item.getSubItemsNr()-1).getRectangle().y+item.getSubItem(item.getSubItemsNr()-1).getRectangle().getHeight()+5);}
        else{line[1] = (int)(item.getRectangle().y+item.getRectangle().getHeight()+5);}
        line[3] = line[1];
        line[4] = (int)(item.getFirstSuitaParent(false).getRectangle().y+item.getFirstSuitaParent(false).getRectangle().getHeight()/2);}
        
    public void lineAfterSuitaParent(Item item, int X){
        line[0] = (int)(item.getTcParent(false).getFirstSuitaParent(false).getRectangle().x-25);
        line[2] = X;
        line[1] = (int)(item.getRectangle().y+item.getRectangle().getHeight()+5);
        line[3] = line[1];
        line[4] = (int)(item.getFirstSuitaParent(false).getRectangle().y+item.getFirstSuitaParent(false).getRectangle().getHeight()/2);}
        
    public void lineAfterTcParent(Item item, int X){
        line[0] = (int)(item.getTcParent(false).getRectangle().x-25);
        line[1] = (int)(item.getTcParent(false).getSubItem(item.getTcParent(false).getSubItemsNr()-1).getRectangle().y+item.getTcParent(false).getSubItem(item.getTcParent(false).getSubItemsNr()-1).getRectangle().getHeight()+5);
        line[2] = X;
        line[3] = line[1];
        line[4] = (int)(item.getTcParent(false).getRectangle().y+item.getTcParent(false).getRectangle().getHeight()/2);}
            
    public void handleDraggingLine(int X, int Y){
        Item item = null;
        item = getUpperItem(X,Y);
        if(item==null){
            line[0] = 0;
            line[1] = 5;
            line[2] = X;
            line[3] = 5;}
        else{
            if(item.getType()==2){//este o suita
                if(item.getRectangle().intersects(new Rectangle(0,Y-1,getWidth(),2))){//daca atinge suita
                    if(item.getSubItemsNr()>0&&item.getSubItem(0).isVisible()){lineInsideSuita(item,X);}//daca aceasta e expanded
                    else{lineOnSuita(item,X);}}//daca aceasta nu e expanded
                else if (item.getSubItemsNr()>0&&item.getSubItem(0).isVisible()){lineInsideSuita(item,X);}//daca nu atinge suita dar aceasta e expanded
                else if(item.getRectangle().y+item.getRectangle().getHeight()+5<=Y){lineAfterUpperParent(item,X);} //este mai jos de 5 pixeli cat sa bage sub suita
                else{lineUnderSuita(item,X);}}//este mai sus de 5 pixeli cat sa bage in suita                
            else if(item.getType()==1){//este un tc
                if(item.getRectangle().intersects(new Rectangle(0,Y-1,getWidth(),2))){//daca atinge tc-ul
                    boolean up = isUpperHalf(item,Y);
                    if(up){lineAboveTc(item,X);}//atinge si este in partea de deasupra deasupra tc-ului
                    else{lineUnderTc(item,X);}}//atinge si este in partea de jos a tc
                else{//nu a atins tc-ul
                    if(item.getFirstSuitaParent(false)!=null&&item.getFirstSuitaParent(false).getSubItemsNr()-1==item.getPos().get(item.getPos().size()-1)){//daca tc-ul are parent si e ultimul din parent
                        if(Y<item.getRectangle().y+item.getRectangle().getHeight()+5){lineUnderTc(item, X);}//5 e jumatate din distante dintre elemente System.out.println("Should be inserted in upper parent");
                        else if(!item.getSubItem(0).isVisible()){lineAfterUpperParent(item,X);}}//trebuie inserat dupa parentul tc-ului de deasupra
                    else{lineUnderTc(item,X);}}}//nu e ultimul tc sau e pe nivelul 0 trebuie inserat in acelasi nivel                        
            else{//este un prop
                if(item.getTcParent(false).getFirstSuitaParent(false)!=null && item.getTcParent(false).getSubItemsNr()-1==item.getPos().get(item.getPos().size()-1) && item.getTcParent(false).getFirstSuitaParent(false).getSubItemsNr()-1==item.getTcParent(false).getPos().get(item.getTcParent(false).getPos().size()-1) && Y>item.getRectangle().y+item.getRectangle().getHeight()+5){//daca prop-ul e ultimul din tc si tc-ul e ultimul din suita si mouseul e mai jos de 5 px fata de prop                                 
                    lineAfterSuitaParent(item,X);}
                else{lineAfterTcParent(item,X);}}}//nu este ultimul prop, se poate adauga dupa tc-ul cu acest prop
        repaint();
        if(dragscroll){
            scrolldown = false;
            scrollup = false; 
            if(Y-Repository.f.p.p1.sc.pane.getVerticalScrollBar().getValue()<10){
                int scrollvalue = Repository.f.p.p1.sc.pane.getVerticalScrollBar().getValue();
                scrolldown = true;
                Repository.f.p.p1.sc.pane.getVerticalScrollBar().setValue(scrollvalue-10);}
            else if(Y-Repository.f.p.p1.sc.pane.getVerticalScrollBar().getValue()>Repository.f.p.p1.sc.pane.getSize().getHeight()-15){
                int scrollvalue = Repository.f.p.p1.sc.pane.getVerticalScrollBar().getValue();
                scrollup = true; 
                Repository.f.p.p1.sc.pane.getVerticalScrollBar().setValue(scrollvalue+10);}}}
            
    public String getArrayString(ArrayList<Integer> selected2){
        StringBuffer string = new StringBuffer();
        for(Integer el:selected2){
            string.append(el.toString()+" ");}
        return string.toString();}
        
    public Item getUpperItem(int X, int Y){
        int y1 = Y;
        Item upper=null;
        while(y1>0){
            for(int x1=0;x1<getWidth();x1+=5){
                getClickedItem(x1,y1);
                if(selected.size()>0){
                    upper=getItem(selected,false);
                    if(upper!=null)break;}
                if(upper!=null)break;}
            y1-=5;}
        return upper;}
            
    public Item nextInLine(Item item){
        if(item.getType()==2&&item.getSubItemsNr()>0&&item.getSubItem(0).isVisible()){//daca e o suita visibila sa coboare un element in subitems
            return item.getSubItem(0);}
        else{
            ArrayList <Integer> temp =(ArrayList <Integer>)item.getPos().clone();
            Item upper;
            if(temp.size()>1){temp.remove(temp.size()-1);
                upper = getItem(temp,false);}
            else{upper = null;}
            if(upper!=null&&upper.getSubItemsNr()-1>item.getPos().get(item.getPos().size()-1)){//mai sunt elemente imediat sub el
                temp =(ArrayList <Integer>)item.getPos().clone();
                temp.set(temp.size()-1,temp.get(temp.size()-1)+1);
                return getItem(temp,false);}
            if(upper==null&&Repository.getSuiteNr()-1>item.getPos().get(item.getPos().size()-1)){
                temp.set(temp.size()-1,temp.get(temp.size()-1)+1);
                return getItem(temp,false);}
            return iterateBack((ArrayList <Integer>)item.getPos().clone());}}
            
    public Item iterateBack(ArrayList <Integer> pos){
        if(pos.size()==1){            
            if(Repository.getSuiteNr()>pos.get(0)+1){
                return Repository.getSuita(pos.get(0)+1);}
            else return null;}
        int index = pos.get(pos.size()-1);
        pos.remove(pos.size()-1);
        Item item = getItem(pos,false);
        if(item.getSubItemsNr()>(index+1))return item.getSubItem(index+1);
        else return iterateBack(pos);}
        
    public Item prevInLine(Item item){//elementul anterio al lui item
        ArrayList <Integer> temp =(ArrayList <Integer>)item.getPos().clone();
        if(item.getPos().get(item.getPos().size()-1)>0){//mai sunt elemente inaintea lui
            temp.set(temp.size()-1,temp.get(temp.size()-1)-1);
            return lastVisible(temp);}
        else if(item.getPos().size()>1){
            temp.remove(temp.size()-1);
            return getItem(temp,false);}
        return null;}
        
    public Item lastVisible(ArrayList <Integer> pos){//ultimul element vizibil in arbore sub pozitie pos
        Item item = getItem(pos,false);
        if(item.getType()==2&&item.getSubItemsNr()>0&&item.getSubItem(0).isVisible()){
            pos.add(new Integer(item.getSubItemsNr()-1));
            return lastVisible(pos);}        
        return item;}
            
    public void printPos(Item item){
        if(item.getType()==1||item.getType()==2){
            System.out.print(item.getName()+" - ");
            for(int i=0;i<item.getPos().size();i++){
                System.out.print(item.getPos().get(i));}
            System.out.println();}
        if(item.getType()==2){
            for(int i=0;i<item.getSubItemsNr();i++){
                printPos(item.getSubItem(i));}}}
                
    public boolean compareArrays(ArrayList<Integer> one, ArrayList<Integer> two){
        if(one.size()!=two.size())return false;
        else{
            for(int i=0;i<one.size();i++){
                if(one.get(i)!=two.get(i))return false;}
            return true;}}
    
    public void handleClick(MouseEvent ev){
        if(ev.getButton()==1){
            if(Repository.getSuiteNr()==0)return;
            if(keypress==0){
                deselectAll();
                getClickedItem(ev.getX(),ev.getY());
                if(selected.size()>0){
                    selectItem(selected);
                    if(getItem(selected,false).getType()==2&&getItem(selected,false).getPos().size()==1){
                        Item temp = getItem(selected,false);
                        int userDefNr = temp.getUserDefNr();
                        Repository.f.p.p1.suitaDetails.setParent(temp);
                        if(userDefNr!=Repository.f.p.p1.suitaDetails.getDefsNr()){
                            System.out.println("Warning, suite "+temp.getName()+" has "+userDefNr+" fields while in bd.xml are defined "+Repository.f.p.p1.suitaDetails.getDefsNr()+" fields");
                            if(Repository.f.p.p1.suitaDetails.getDefsNr()<userDefNr){
                                temp.getUserDefs().subList(Repository.f.p.p1.suitaDetails.getDefsNr(),userDefNr).clear();}}
                        try{    
                            for(int i=0;i<Repository.f.p.p1.suitaDetails.getDefsNr();i++){
                                if(temp.getUserDefNr()==i)break;
                                Repository.f.p.p1.suitaDetails.getDefPanel(i).setDecription(temp.getUserDef(i)[1]);}}
                        catch(Exception e){e.printStackTrace();}}
                    if(getItem(selected,false).getCheckRectangle().intersects(new Rectangle(ev.getX()-1,ev.getY()-1,2,2))){
                        getItem(selected,false).setCheck(!getItem(selected,false).getCheck());}
                    else if(getItem(selected,false).getSubItemsNr()>0&&ev.getClickCount()==2){
                        if(getItem(selected,false).getType()==2 && !getItem(selected,false).getSubItem(0).isVisible()){getItem(selected,false).setVisibleTC();}
                        else getItem(selected,false).setVisible(!(getItem(selected,false).getSubItem(0).isVisible()));}
                    updateLocations(getItem(selected,false));}
                repaint();}
            else if(keypress==2){
                getClickedItem(ev.getX(),ev.getY());
                int [] theone = new int[selected.size()];
                for(int i=0;i<selected.size();i++){theone[i]= selected.get(i).intValue();}
                Item theone1 = getItem(selected,false);
                theone1.select(!theone1.isSelected());
                if(theone1.isSelected())selectedcolection.add(theone);
                else{
                    for(int m=0;m<selectedcolection.size();m++){
                        if(Arrays.equals(selectedcolection.get(m),theone)){
                            selectedcolection.remove(m);
                            break;}}}
                repaint();}
            else{// selectia in caz ca are shift
                deselectAll();
                int [] theone1 = new int[selected.size()];
                for(int i=0;i<selected.size();i++){theone1[i]= selected.get(i).intValue();}
                getClickedItem(ev.getX(),ev.getY());
                int [] theone2 = new int[selected.size()];
                for(int i=0;i<selected.size();i++){theone2[i]= selected.get(i).intValue();}
                if(theone1.length==theone2.length){
                    if(theone1.length>1){
                        int [] temp1,temp2;
                        temp1 = Arrays.copyOfRange(theone1,0,theone1.length-1);
                        temp2 = Arrays.copyOfRange(theone2,0,theone2.length-1);
                        if(Arrays.equals(temp1,temp2)){
                            int [] first,second;
                            if(theone2[theone2.length-1]>=theone1[theone1.length-1]){
                                first = theone2;
                                second = theone1;}
                            else{
                                first = theone1;
                                second = theone2;}
                            ArrayList<Integer>temp11 = new ArrayList<Integer>();
                            for(int i=0;i<temp1.length;i++)temp11.add(new Integer(temp1[i]));
                            Item parent = getItem(temp11,false);
                            for(int i=second[second.length-1];i<first[first.length-1]+1;i++){
                                parent.getSubItem(i).select(true);
                                int [] temporary = new int[parent.getSubItem(i).getPos().size()];
                                for(int m=0;m<temporary.length;m++)temporary[m]=parent.getSubItem(i).getPos().get(m).intValue();
                                selectedcolection.add(temporary);}}}
                    else{
                        int first,second;
                        if(theone1[0]>=theone2[0]){
                            first = theone1[0];
                            second = theone2[0];}
                        else{
                            second = theone1[0];
                            first = theone2[0];}
                        for(int m=second;m<first+1;m++){
                            Repository.getSuita(m).select(true);
                            selectedcolection.add(new int[]{m});}}}
            repaint();}}
        if(ev.getButton()==3){ 
            getClickedItem(ev.getX(),ev.getY());            
            if((selected.size()==0)){
                if(Repository.getSuiteNr()>0){
                    deselectAll();                    
                    repaint();}
                noSelectionPopUp(ev);}
            else{if(!getItem(selected,false).isSelected()){
                    deselectAll();
                    selectItem(selected);
                    repaint();
                    if(getItem(selected,false).getType()==0) propertyPopUp(ev);
                    else if(getItem(selected,false).getType()==1) tcPopUp(ev,getItem(selected,false));
                    else suitaPopUp(ev,getItem(selected,false));}
                else{if(selectedcolection.size()==1){
                        if(getItem(selected,false).getType()==0) propertyPopUp(ev);
                        else if(getItem(selected,false).getType()==1) tcPopUp(ev,getItem(selected,false));
                        else suitaPopUp(ev,getItem(selected,false));}
                    else{multipleSelectionPopUp(ev);}}}}}    
                    
    public void noSelectionPopUp(final MouseEvent ev){ //poup in caz ca nu s-a selectat nimic, pozitia unde s-a facut click
        p.removeAll();
        JMenuItem item = new JMenuItem("Add Suite");        
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev2){
                int y1 = ev.getY();
                Item upper=null;
                while(y1>0){
                    y1-=5;
                    getClickedItem(ev.getX(),y1);
                    if(selected.size()>0){
                            upper=getItem(selected,false);
                        if(upper!=null){
                            break;}}}
                if(upper!=null&&upper.getType()==1){
                    int index = upper.getPos().get(upper.getPos().size()-1).intValue();
                    int position = upper.getPos().size()-1;
                    ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone();
                    if(temp.size()>1)temp.remove(temp.size()-1);
                    Item parent = getItem(temp,false);
                    for(int j = upper.getPos().get(upper.getPos().size()-1).intValue()+1;j<parent.getSubItemsNr();j++){   
                        parent.getSubItem(j).updatePos(position,new Integer(parent.getSubItem(j).getPos().get(position).intValue()+1));}
                    (new AddSuiteFrame(Repository.f.p.p1.sc.g, parent,index+1)).setLocation(ev.getX()-50,ev.getY()-50);}
                else (new AddSuiteFrame(Repository.f.p.p1.sc.g, null,0)).setLocation((int)ev.getLocationOnScreen().getX()-50,(int)ev.getLocationOnScreen().getY()-50);}});// adauga suita           
        item = new JMenuItem("Open XML");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                JFileChooser chooser = new JFileChooser(); 
                chooser.setFileFilter(new XMLFilter());
                chooser.setCurrentDirectory(new java.io.File("."));
                chooser.setDialogTitle("Select XML File"); 
                if (chooser.showOpenDialog(Repository.f) == JFileChooser.APPROVE_OPTION) {                     
                    Repository.emptyRepository();
                    parseXML(chooser.getSelectedFile());}}});// de deschis local un xml                
        item = new JMenuItem("Save suite XML");
        p.add(item);        
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(!user.equals(""))printXML(user,false);}});//de salvat xml user         
        p.show(this,ev.getX(),ev.getY());}
        
    public void propertyPopUp(MouseEvent ev){//popup pentru click pe property, locatia unde s-a facut click
        p.removeAll();        
        JMenuItem item = new JMenuItem("Redefine Propertie");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){}});     
            p.show(this,ev.getX(),ev.getY());}            
           
    public void multipleSelectionPopUp(MouseEvent ev){//popup pentru click pe property, locatia unde s-a facut click
        p.removeAll();        
        JMenuItem item = new JMenuItem("Remove");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeSelected();}});
            p.show(this,ev.getX(),ev.getY());}  
            
    public void tcPopUp(MouseEvent ev, final Item tc){
        p.removeAll();
        JMenuItem item;
        item = new JMenuItem("Add Property");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                JTextField name = new JTextField();   
                JTextField value = new JTextField();
                Object[] message = new Object[] {"Name", name, "Value", value};
            int r = JOptionPane.showConfirmDialog(Repository.f.p.p1.sc.g, message, "Property: value", JOptionPane.OK_CANCEL_OPTION);
                if(r == JOptionPane.OK_OPTION){
                    ArrayList <Integer> indexpos3 = (ArrayList <Integer>)tc.getPos().clone();
                    indexpos3.add(new Integer(tc.getSubItemsNr()));
                    FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", 0, 11));
                    int width = metrics.stringWidth(name.getText()+":  "+value.getText()) + 8;
                    Item property = new Item(name.getText(),0,-1,-1,width+30,20,indexpos3);
                    property.setValue(value.getText());
                    if(!tc.getSubItem(0).isVisible())property.setSubItemVisible(false);
                    tc.addSubItem(property);
                    updateLocations(tc);
                    repaint();}}});
        item = new JMenuItem("Rename TC");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                String name = JOptionPane.showInputDialog(Repository.f.p.p1.sc.g,"Please enter the TC name","Suite Name",  JOptionPane.PLAIN_MESSAGE);
                FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 13));
                int width = metrics.stringWidth(name);
                tc.setName(name);
                tc.getRectangle().setSize(width+40,(int)tc.getRectangle().getHeight());
                updateLocations(tc);
                repaint();}});
        item = new JMenuItem("Expand TC");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                tc.setVisible(true);
                updateLocations(tc);
                repaint();}});
        item = new JMenuItem("Contract TC");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                tc.setVisible(false);
                updateLocations(tc);
                repaint();}});
        item = new JMenuItem("Switch Runnable");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                tc.switchRunnable();
                repaint();}});
        item = new JMenuItem("Remove TC");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                removeTC(tc);
                selectedcolection.clear();}});
        p.show(this,ev.getX(),ev.getY());}        
        
    public void suitaPopUp(MouseEvent ev,final Item suita){
        p.removeAll();
        JMenuItem item ;
        item = new JMenuItem("add Suita");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                new AddSuiteFrame(Repository.f.p.p1.sc.g, suita,0);}});
        p.add(item);        
        if(suita.getPos().size()==1){
            item = new JMenuItem("EpID");
            p.add(item);
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    try{File f = new File(Repository.temp+System.getProperty("file.separator")+"Twister"+System.getProperty("file.separator")+"EpID.txt");
                        String line = null;  
                        InputStream in = Repository.c.get(Repository.REMOTEEPIDDIR);
                        InputStreamReader inputStreamReader = new InputStreamReader(in);
                        BufferedReader bufferedReader = new BufferedReader(inputStreamReader);  
                        StringBuffer b=new StringBuffer("");
                        while ((line=bufferedReader.readLine())!= null){b.append(line+";");}                        
                        bufferedReader.close();
                        inputStreamReader.close();
                        in.close();
                        String result = b.toString();
                        String  [] vecresult = result.split(";");
                        try{String ID = (String)JOptionPane.showInputDialog(Repository.f.p.p1.sc.g,"Please select an EpID","EpID's", JOptionPane.INFORMATION_MESSAGE,null, vecresult,"EpID's");
                            suita.setEpId(ID);
                            for(int i=0;i<suita.getSubItemsNr();i++){
                                assignEpID(suita.getSubItem(i),ID);}
                            repaint();}
                        catch(Exception e){e.printStackTrace();}}
                    catch(Exception e){e.printStackTrace();}}});}
        item = new JMenuItem("Rename Suite");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){                
            String name = JOptionPane.showInputDialog(Repository.f.p.p1.sc.g,"Please enter the suite name","Suite Name",  JOptionPane.PLAIN_MESSAGE).toUpperCase();
            FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 14));
            int width = metrics.stringWidth(name)+140;
            suita.setName(name);
            suita.getRectangle().setSize(width,(int)suita.getRectangle().getHeight());
            if(suita.isVisible())updateLocations(suita);
            repaint();}});
        item = new JMenuItem("Expand all");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                suita.setVisible(true);
                updateLocations(suita);
                repaint();}});
        item = new JMenuItem("Contract All");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                int nr = suita.getSubItemsNr();
                for(int i=0;i<nr;i++){
                    suita.getSubItem(i).setVisible(false);}
                updateLocations(suita);
                repaint();}});
        item = new JMenuItem("Remove Suite");
        p.add(item);
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if(suita.getPos().size()==1){//este pe nivelul 0
                    int index = suita.getPos().get(0).intValue();
                    Repository.getSuite().remove(suita);                    
                    if(Repository.getSuiteNr()>=index){
                        for(int i= index;i<Repository.getSuiteNr();i++){
                            Repository.getSuita(i).updatePos(0,new Integer(Repository.getSuita(i).getPos().get(0).intValue()-1));}
                    if(Repository.getSuiteNr()>0){
                        Repository.getSuita(0).setLocation(new int[]{5,10});
                        updateLocations(Repository.getSuita(0));}
                    repaint();
                    selectedcolection.clear();}}
                else{int index = suita.getPos().get(suita.getPos().size()-1).intValue();//nu e pe nivelul 0
                    int position = suita.getPos().size()-1;
                    ArrayList<Integer> temp = (ArrayList<Integer>)suita.getPos().clone();
                    temp.remove(temp.size()-1);
                    Item parent = getItem(temp,false);
                    parent.getSubItems().remove(suita);                    
                    if(parent.getSubItemsNr()>=index){
                        for(int i = index;i<parent.getSubItemsNr();i++){
                            parent.getSubItem(i).updatePos(position,new Integer(parent.getSubItem(i).getPos().get(position).intValue()-1));}}
                    updateLocations(parent);
                    repaint();
                    selectedcolection.clear();}}});     
        p.show(this,ev.getX(),ev.getY());} 
        
    public void setCanRequestFocus(boolean canrequestfocus){
        this.canrequestfocus = canrequestfocus;}
        
        
        
//         de vazut sa nu stearga propurile
        
    public void removeSelected(){        
        if(selectedcolection.size()>0){
            ArrayList<Item> fordeletion = new ArrayList<Item>();                
            int selectednr = selectedcolection.size();
            for(int i=0;i<selectednr;i++){
                ArrayList<Integer> temp = new ArrayList<Integer>();
                int indexsize = selectedcolection.get(i).length;
                for(int j=0;j<indexsize;j++){temp.add(new Integer(selectedcolection.get(i)[j]));}
                Item theone = getItem(temp,false);
                if(theone.getType()!=0)fordeletion.add(theone);}
            ArrayList<Item> unnecessary = new ArrayList<Item>();
            for(int i=0;i<fordeletion.size();i++){
                Item one = fordeletion.get(i);
                ArrayList<Integer>pos = (ArrayList<Integer>)one.getPos().clone();
                if(pos.size()>1){
                    pos.remove(pos.size()-1);
                    Item parent = getItem(pos,false);
                    if(parent.isSelected()){unnecessary.add(fordeletion.get(i));}}}
            for(int i=0;i<unnecessary.size();i++){fordeletion.remove(unnecessary.get(i));}
            int deletenr = fordeletion.size();
            for(int i=0;i<deletenr;i++){
                Item theone = fordeletion.get(i);
                if(theone.getPos().size()==1){
                    int index = theone.getPos().get(0).intValue();
                    Repository.getSuite().remove(theone);                    
                    if(Repository.getSuiteNr()>=index){
                        for(int k= index;k<Repository.getSuiteNr();k++){
                            Repository.getSuita(k).updatePos(0,new Integer(Repository.getSuita(k).getPos().get(0).intValue()-1));}}}
                else{            
                    int index = theone.getPos().get(theone.getPos().size()-1).intValue();
                    int position = theone.getPos().size()-1;
                    ArrayList<Integer> temporary = (ArrayList<Integer>)theone.getPos().clone();
                    temporary.remove(temporary.size()-1);
                    Item parent = getItem(temporary,false);
                    parent.getSubItems().remove(theone);                    
                    if(parent.getSubItemsNr()>=index){
                        for(int k = index;k<parent.getSubItemsNr();k++){
                            parent.getSubItem(k).updatePos(position,new Integer(parent.getSubItem(k).getPos().get(position).intValue()-1));}}}}
            if(Repository.getSuiteNr()>0){
                Repository.getSuita(0).setLocation(new int[]{5,10});
                updateLocations(Repository.getSuita(0));}
            repaint();
            selectedcolection.clear();}}
        
    public void assignEpID(Item item,String ID){
        if(item.getType()==2){
            item.setEpId(ID);
            for(int i=0;i<item.getSubItemsNr();i++){assignEpID(item.getSubItem(i),ID);}}}                
                
    public void removeTC(Item tc){ 
        if(tc.getPos().size()>1){//tc nu e pe nivelul 0
            int index = tc.getPos().get(tc.getPos().size()-1).intValue();
            int position = tc.getPos().size()-1;
            ArrayList<Integer> temp = (ArrayList<Integer>)tc.getPos().clone();
            temp.remove(temp.size()-1);
            Item parent = getItem(temp,false);
            parent.getSubItems().remove(tc);                    
            if(parent.getSubItemsNr()>=index){
                for(int i = index;i<parent.getSubItemsNr();i++){
                    parent.getSubItem(i).updatePos(position,new Integer(parent.getSubItem(i).getPos().get(position).intValue()-1));}}
            updateLocations(parent);
            repaint();}
        else{//tc pe nivelul 0    
            int index = tc.getPos().get(0).intValue();
            Repository.getSuite().remove(tc);                    
            if(Repository.getSuiteNr()>=index){
                for(int i= index;i<Repository.getSuiteNr();i++){
                    Repository.getSuita(i).updatePos(0,new Integer(Repository.getSuita(i).getPos().get(0).intValue()-1));}
            if(Repository.getSuiteNr()>0){
                Repository.getSuita(0).setLocation(new int[]{5,10});
                updateLocations(Repository.getSuita(0));}
            repaint();
            selectedcolection.clear();}}}
        
    public void deselectAll(){
        int selectednr = selectedcolection.size()-1;
        for(int i=selectednr ; i>=0 ; i--){
            int [] itemselected = selectedcolection.get(i);
            Item theone = Repository.getSuita(itemselected[0]);
            for(int j=1;j<itemselected.length;j++){theone = theone.getSubItem(itemselected[j]);}
            theone.select(false);
            selectedcolection.remove(i);}}
            
    public void selectItem(ArrayList <Integer> pos){
        getItem(pos,false).select(true);
        int [] theone1 = new int[pos.size()];
        for(int i=0;i<pos.size();i++){theone1[i]= pos.get(i).intValue();}
        selectedcolection.add(theone1);}
    
    public void getClickedItem(int x, int y){
        Rectangle r = new Rectangle(x-1,y-1,2,2);
        int suitenr = Repository.getSuiteNr();
        selected = new ArrayList<Integer>();
        for(int i=0;i<suitenr;i++){
            if(handleClicked(r,Repository.getSuita(i))){
                selected.add(i);
                break;}}
        if(selected.size()>0)Collections.reverse(selected);}
        
    public static Item getItem(ArrayList <Integer> pos,boolean test){           
        Item theone1;
        if(!test)theone1 = Repository.getSuita(pos.get(0));
        else theone1 = Repository.getTestSuita(pos.get(0));
        for(int j=1;j<pos.size();j++){
            theone1 = theone1.getSubItem(pos.get(j));}
        return theone1;}
    
    public boolean handleClicked(Rectangle r, Item item){
        if(r.intersects(item.getRectangle())&&item.isVisible())return true;
        else{int itemnr = item.getSubItemsNr();
            for(int i=0;i<itemnr;i++){
                if(handleClicked(r,item.getSubItem(i))){
                    selected.add(i);
                    return true;}}
            return false;}}
        
    public void updateLocations(Item suita){
        ArrayList <Integer> selected2 = (ArrayList <Integer>)suita.getPos().clone();
        if(selected2.size()>1){
            int index = selected2.get(0);
            selected2.remove(0);
            for(int i=index;i<Repository.getSuiteNr();i++){  
                Repository.f.p.p1.sc.g.iterateThrough(Repository.getSuita(i),selected2);
                selected2 = null;}}
        else if(selected2.size()==1){
            for(int i=selected2.get(0);i<Repository.getSuiteNr();i++){
                Repository.f.p.p1.sc.g.iterateThrough(Repository.getSuita(i),null);}}
        y=10;
        foundfirstitem=false;
        updateScroll();}
            
    public int calcPreviousPositions(Item item){
        ArrayList <Integer> pos = (ArrayList <Integer>)item.getPos().clone();
        if(pos.size()>1){
            pos.remove(pos.size()-1);
            Item temp = getItem(pos,false);
            if(temp.getType()==2) return temp.getLocation()[0]+(int)((temp.getRectangle().getWidth()-100)/2+20);
            return temp.getLocation()[0]+(int)(temp.getRectangle().getWidth()/2+20);}
        else{return 5;}}
    
    public void positionItem(Item item){        
        int x = calcPreviousPositions(item);
        item.setLocation(new int[]{x,y});
        y+=(int)(10+item.getRectangle().getHeight());}
    
    public void iterateThrough(Item item, ArrayList <Integer> theone){
        int subitemsnr = item.getSubItemsNr();
        if(theone==null){
            if(item.isVisible()){
                if(!foundfirstitem)y=item.getLocation()[1];
                foundfirstitem = true;
                positionItem(item);}
            for(int i=0;i<subitemsnr;i++){    
                iterateThrough(item.getSubItem(i),null);}}
        else if(theone.size()>1){
            int index = theone.get(0);
            theone.remove(0);
            for(int i=index;i<subitemsnr;i++){
                iterateThrough(item.getSubItem(i),theone);
                theone=null;}}
        else if(theone.size()==1){
            int index = theone.get(0);
            for(int i=index;i<subitemsnr;i++){
                iterateThrough(item.getSubItem(i),null);}}}
            
    public void paint(Graphics g){
        g.setColor(Color.WHITE);
        g.fillRect(0,0,getWidth(),getHeight());
        drawDraggingLine(g);
        g.setColor(Color.BLACK);
        int suitenr = Repository.getSuiteNr();
        for(int i=0;i<suitenr;i++){
            handlePaintItem(Repository.getSuita(i),g);}}
        
    public void drawDraggingLine(Graphics g){
        if(line[0]!=-1){
            g.setColor(new Color(150,150,150));
            g.drawLine(line[0],line[1],line[2],line[3]);
            g.drawLine(line[0],line[3],line[0],line[4]);}}
    
    public void handlePaintItem(Item item, Graphics g){
        drawItem(item,g);
        int subitemnr = item.getSubItemsNr();
        if(subitemnr>0&&item.getSubItem(0).isVisible()){
            for(int i=0;i<subitemnr;i++){handlePaintItem(item.getSubItem(i),g);}}}
        
    public void drawItem(Item item,Graphics g){
        g.setFont(new Font("TimesRoman", Font.PLAIN, 12));
        g.setColor(Color.BLACK);
        if(item.isSelected()){
            g.setColor(new Color(220,220,220));
            g.fillRect((int)item.getRectangle().getX(),(int)item.getRectangle().getY(),(int)item.getRectangle().getWidth(),(int)item.getRectangle().getHeight());
            g.setColor(Color.BLACK);
            g.drawRect((int)item.getRectangle().getX(),(int)item.getRectangle().getY(),(int)item.getRectangle().getWidth(),(int)item.getRectangle().getHeight());}
        if(item.getType()==2){
            g.drawString(item.getName(),(int)item.getRectangle().getX()+45,(int)item.getRectangle().getY()+18);
            g.drawImage(Repository.getSuitaIcon(),(int)item.getRectangle().getX()+25,(int)item.getRectangle().getY()+1,null);}
        else if(item.getType()==1){
            if(!item.isRunnable())g.setColor(Color.GRAY);
            g.drawString(item.getName(),(int)item.getRectangle().getX()+50,(int)item.getRectangle().getY()+15);
            g.setColor(Color.BLACK);
            g.drawImage(Repository.getTCIcon(),(int)item.getRectangle().getX()+25,(int)item.getRectangle().getY()+1,null);}
        else{if(item.getPos().get(item.getPos().size()-1).intValue()==0)g.drawImage(Repository.getPropertyIcon(),(int)item.getRectangle().getX()+2,(int)item.getRectangle().getY()+1,null);
            g.drawString(item.getName()+" : "+item.getValue(),(int)item.getRectangle().getX()+25,(int)item.getRectangle().getY()+15);}
        if((item.getPos().size()!=1)){
            if(item.getType()==0 && item.getPos().get(item.getPos().size()-1).intValue()!=0){}
            else{g.setColor(new Color(180,180,180));
                g.drawLine((int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),(int)item.getRectangle().getX(),(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2));
                ArrayList<Integer> temp = (ArrayList<Integer>)item.getPos().clone();
                if(temp.get(temp.size()-1)==0)g.drawLine((int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),(int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY())-5);
                else{temp.set(temp.size()-1,new Integer(temp.get(temp.size()-1).intValue()-1));
                    Item theone = getItem(temp,false);
                    g.drawLine((int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),(int)item.getRectangle().getX()-25,(int)(theone.getRectangle().getY()+theone.getRectangle().getHeight()/2));}
                g.setColor(Color.BLACK);}}
        if(item.getType()!=0){
            g.drawRect((int)item.getCheckRectangle().getX(),(int)item.getCheckRectangle().getY(),(int)item.getCheckRectangle().getWidth(),(int)item.getCheckRectangle().getHeight());
            if(item.getCheck()){
                Rectangle r = item.getCheckRectangle();
                int x2[] = {(int)r.getX(),(int)r.getX()+(int)r.getWidth()/2,(int)r.getX()+(int)r.getWidth(),(int)r.getX()+(int)r.getWidth()/2};
                int y2[] = {(int)r.getY()+(int)r.getHeight()/2,(int)r.getY()+(int)r.getHeight(),(int)r.getY(),(int)r.getY()+(int)r.getHeight()-5};
                g.fillPolygon(x2,y2,4);}}
        if(item.getEpId()!=null){
            g.setFont(new Font("TimesRoman", Font.PLAIN, 11));
            g.drawString(" - "+item.getEpId(),(int)(item.getRectangle().getX()+item.getRectangle().getWidth()-100),(int)(item.getRectangle().getY()+18));}}
        
    public void setUser(String user){//schimba userul si modifica numele din tab conform cu cel al userului
        Repository.f.p.p1.setOpenedfile(new File(user).getName());
        Repository.f.p.p1.suitaDetails.clearDefs();
        Repository.f.p.p1.suitaDetails.setParent(null);
        this.user = user;}
    
    public String getUser(){// metoda pentru aflarea path-ului fisierului xml pentru user
        return user;}        
        
    public void parseXML(File file){//citeste xml si il reprezinta grafic
        new XMLReader(file).parseXML(getGraphics(),false);}
        
    public void printXML(String user, boolean skip){//scrie xml-ul in fisier , in caz ca e skip true e vorba de xml-ul final, in caz contrar
        XMLBuilder xml = new XMLBuilder(Repository.getSuite());//e xml-ul userului
        xml.createXML(skip);
        xml.writeXMLFile(user);}
        
    public int countSubtreeNr(int nr, Object child){
        boolean cond; //tine cont daca e un director sau un fisier
        cond = Repository.f.p.p1.ep.tree.getModel().isLeaf((TreeNode)child);
        ArrayList <TreeNode>list = new ArrayList<TreeNode>();        
        while ((TreeNode)child != null) {
            list.add((TreeNode)child);
            child = ((TreeNode)child).getParent();}
        Collections.reverse(list);
        child = new TreePath(list.toArray());
        if(cond){return nr+1;}
        else{int nr1 = Repository.f.p.p1.ep.tree.getModel().getChildCount(((TreePath)child).getLastPathComponent());
            for(int j=0;j<nr1;j++){
                nr = countSubtreeNr(nr,Repository.f.p.p1.ep.tree.getModel().getChild((TreeNode)((TreePath)child).getLastPathComponent(),j));}
        return nr;}}
        
    public void drop(int x, int y){
        deselectAll();
        requestFocus();
        int max = Repository.f.p.p1.ep.getSelected().length;
        if(max>0){
            for(int i=0;i<max;i++){
                boolean cond = Repository.f.p.p1.ep.tree.getModel().isLeaf((TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent());//nu are copii                
                if(cond){
                    String name = Repository.f.p.p1.ep.getSelected()[i].getPath()[Repository.f.p.p1.ep.getSelected()[i].getPathCount()-2]+"/"+Repository.f.p.p1.ep.getSelected()[i].getPath()[Repository.f.p.p1.ep.getSelected()[i].getPathCount()-1];
                    name = name.split(Repository.getTestSuitePath())[1];
                    FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.PLAIN, 13));
                    Item newItem = new Item(name,1, -1, -1, metrics.stringWidth(name)+48, 20, null);
                    ArrayList<Integer> pos = new ArrayList <Integer>();
                    pos.add(new Integer(0));
                    ArrayList<Integer> pos2 = (ArrayList <Integer>)pos.clone();
                    pos2.add(new Integer(0));
                    Item property = new Item("Running",0,-1,-1,(metrics.stringWidth("Running:  true"))+28,20,pos2);
                    property.setValue("true");
                    newItem.addSubItem(property);
                    newItem.setVisible(false);
                    clone.add(newItem);}
                else{
                    subtreeTC((TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent(),null,0);}}
            handleMouseDroped(y);
            clone.clear();}
//         int max = Repository.f.p.p1.ep.getSelected().length;
//         deselectAll();
//         requestFocus();
//         getClickedItem(x,y);  
//         Item item=null;
//         if(selected.size()!=0)item = getItem(selected,false);
//         if(item!=null&&item.getType()==2){
//             String f,tcf;
//             //int max = Repository.f.p.p1.ep.getSelected().length;  
//             for(int i=0;i<max;i++){
//                 boolean cond = Repository.f.p.p1.ep.tree.getModel().isLeaf((TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent());                
//                 if(cond){
//                     int position = item.getPos().size();
//                     for(int j = 0;j<item.getSubItemsNr();j++){
//                         item.getSubItem(j).updatePos(position,new Integer(item.getSubItem(j).getPos().get(position).intValue()+1));}
//                     ArrayList<Integer> selected2 = (ArrayList<Integer>)item.getPos().clone();
//                     selected2.add(new Integer(0));
//                     insertNewTC(Repository.f.p.p1.ep.getSelected()[i].getPath()[Repository.f.p.p1.ep.getSelected()[i].getPathCount()-2]+"/"+Repository.f.p.p1.ep.getSelected()[i].getPath()[Repository.f.p.p1.ep.getSelected()[i].getPathCount()-1],selected2,item,null);}
//                 else{
//                     int nr = countSubtreeNr(0,(TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent());
//                     int position = item.getPos().size();
//                     for(int j = 0;j<item.getSubItemsNr();j++){
//                         item.getSubItem(j).updatePos(position,new Integer(item.getSubItem(j).getPos().get(position).intValue()+nr));}
//                     subtreeTC((TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent(),item,0);
//                     updateLocations(item);}}
//             updateLocations(getItem(selected,false));
//             repaint();}
//         else if(item!=null&&item.getType()==1){
//             boolean upper = isUpperHalf(item, y);
//             int y1=y;
//             while(true){
//                 if(upper)y1-=2;
//                 else y1+=2;
//                 getClickedItem(x,y1);
//                 if(selected.size()==0){
//                     drop(x,y1);
//                     break;}}}
//         else{
//             if(item==null){
//                 int y1=y;
//                 Item upper=null;
//                 while(y1>0){
//                     y1-=5;
//                     getClickedItem(x,y1);
//                     if(selected.size()>0){
//                         upper=getItem(selected,false);
//                         if(upper!=null){break;}}}
//                 if(upper!=null){
//                     int index = upper.getPos().get(upper.getPos().size()-1).intValue();
//                     int position = upper.getPos().size()-1;
//                     ArrayList<Integer> temp = (ArrayList<Integer>)upper.getPos().clone();
//                     if(temp.size()>1)temp.remove(temp.size()-1);
//                     Item parent = getItem(temp,false);                    
//                     //int max = Repository.f.p.p1.ep.getSelected().length;
//                     if(upper.getType()!=0){
//                         if(upper.getPos().size()>1){
//                             for(int i=0;i<max;i++){
//                                 boolean cond = Repository.f.p.p1.ep.tree.getModel().isLeaf((TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent());
//                                 if(cond){
//                                     int temp1 = index+1;
//                                     for(int j = temp1;j<parent.getSubItemsNr();j++){parent.getSubItem(j).updatePos(position,new Integer(parent.getSubItem(j).getPos().get(position).intValue()+1));}
//                                     ArrayList<Integer> selected2 = (ArrayList<Integer>)upper.getPos().clone();
//                                     selected2.set(selected2.size()-1,new Integer(selected2.get(selected.size()-1).intValue()+1));
//                                     insertNewTC(Repository.f.p.p1.ep.getSelected()[i].getPath()[Repository.f.p.p1.ep.getSelected()[i].getPathCount()-2]+"/"+Repository.f.p.p1.ep.getSelected()[i].getPath()[Repository.f.p.p1.ep.getSelected()[i].getPathCount()-1],selected2,parent,null);}
//                                 else{int nr = countSubtreeNr(0,(TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent());
//                                     int temp1 = index+1;                                   
//                                     for(int j = temp1;j<parent.getSubItemsNr();j++){
//                                         parent.getSubItem(j).updatePos(position,new Integer(parent.getSubItem(j).getPos().get(position).intValue()+nr));}
//                                     subtreeTC((TreeNode)Repository.f.p.p1.ep.getSelected()[i].getLastPathComponent(),parent,upper.getPos().get(upper.getPos().size()-1).intValue()+1+i);}}
//                                updateLocations(parent);}
//                         else{drop((int)upper.getLocation()[0]+2,(int)upper.getLocation()[1]+2);}}
//                     repaint();}}}
                
                }
        
    public int subtreeTC(Object child, Item parent, int location){
        boolean cond; //tine cont daca e un director sau un fisier
        cond = Repository.f.p.p1.ep.tree.getModel().isLeaf((TreeNode)child);
        ArrayList <TreeNode>list = new ArrayList<TreeNode>();        
        while ((TreeNode)child != null){
            list.add((TreeNode)child);
            child = ((TreeNode)child).getParent();}
        Collections.reverse(list);
        child = new TreePath(list.toArray());
        if(cond){
            if(parent==null){//daca este chemat din dropul jtree
                String name = ((TreePath)child).getPath()[((TreePath)child).getPathCount()-2]+"/"+((TreePath)child).getPath()[((TreePath)child).getPathCount()-1];
                name = name.split(Repository.getTestSuitePath())[1];
                FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.PLAIN, 13));
                Item newItem = new Item(name,1, -1, -1, metrics.stringWidth(name)+48, 20, null);
                ArrayList<Integer> pos = new ArrayList <Integer>();
                pos.add(new Integer(0));
                ArrayList<Integer> pos2 = (ArrayList <Integer>)pos.clone();
                pos2.add(new Integer(0));
                Item property = new Item("Running",0,-1,-1,(metrics.stringWidth("Running:  true"))+28,20,pos2);
                property.setValue("true");
                newItem.addSubItem(property);
                newItem.setVisible(false);
                clone.add(newItem);
                return 0;}
            addNewTC(((TreePath)child).getPath()[((TreePath)child).getPathCount()-2]+"/"+((TreePath)child).getPath()[((TreePath)child).getPathCount()-1],parent,location);
            return location+1;}
        else{int nr = Repository.f.p.p1.ep.tree.getModel().getChildCount(((TreePath)child).getLastPathComponent());
            for(int j=0;j<nr;j++){
                location = subtreeTC(Repository.f.p.p1.ep.tree.getModel().getChild((TreeNode)((TreePath)child).getLastPathComponent(),j),parent,location);}
            return location;}}
        
    public void addNewTC(String file,Item parent,int location){// adauga un nou tc, accepta un file care este tc-ul si pozitia suitei in vector
        file = file.split(Repository.getTestSuitePath())[1];
        FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.PLAIN, 13));
        ArrayList <Integer> indexpos = (ArrayList <Integer>)parent.getPos().clone();
        indexpos.add(new Integer(location));
        Item tc = new Item(file,1,-1,-1,metrics.stringWidth(file)+48,20,indexpos);
        ArrayList <Integer> indexpos2 = (ArrayList <Integer>)indexpos.clone();
        indexpos2.add(new Integer(0));
        Item property = new Item("Running",0,-1,-1,(metrics.stringWidth("Running:  true"))+28,20,indexpos2);
        property.setValue("true");
        tc.addSubItem(property);
        if(parent.getSubItemsNr()>0){if(!parent.getSubItem(0).isVisible())tc.setSubItemVisible(false);}
        tc.setVisible(false);
        parent.insertSubItem(tc,location);}
        
    public void insertNewTC(String file,ArrayList <Integer> pos,Item parent,Item item){// adauga un nou tc, accepta un file care este tc-ul si pozitia suitei in vector
        Item tc = null;
        if(item==null){
            file = file.split(Repository.getTestSuitePath())[1];
            FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.PLAIN, 13));
            tc = new Item(file,1,-1,-1,metrics.stringWidth(file)+48,20,pos);
            ArrayList<Integer>pos2 = (ArrayList <Integer>)pos.clone();
            pos2.add(new Integer(0));
            Item property = new Item("Running",0,-1,-1,(metrics.stringWidth("Running:  true"))+28,20,pos2);
            property.setValue("true");
            tc.addSubItem(property);
            tc.setVisible(false);}
        else{tc=item;
            tc.selectAll(tc, false);}
        if(parent.getSubItemsNr()>0)if(!parent.getSubItem(0).isVisible())tc.setSubItemVisible(false);
        parent.insertSubItem(tc,pos.get(pos.size()-1));
        updateLocations(parent);
        repaint();}
        
    public int getLastY(Item item, int height){
        if(height<=(item.getRectangle().getY()+item.getRectangle().getHeight())){
            height=(int)(item.getRectangle().getY()+item.getRectangle().getHeight());        
            int nr = item.getSubItemsNr()-1;
            for(int i=nr;i>=0;i--){
                if(item.getSubItem(i).isVisible()){height = getLastY(item.getSubItem(i),height);}}
            return height;}
        else return height;}
        
    public void updateScroll(){//updatarea scrollului in cazul in care s-a modificat dimensiunea graficului
        int y1=0;
        for(int i=0;i<Repository.getSuiteNr();i++){
            if(Repository.getSuita(i).isVisible())y1 = getLastY(Repository.getSuita(i),y1);}
        if(y1>getHeight()){
            setPreferredSize(new Dimension(425,y1+10));
            revalidate();}
        if(getHeight()>595){
            if(y1<getHeight()-10){
                setPreferredSize(new Dimension(425,y1+10));
                revalidate();}
            if(y1<595){
                setPreferredSize(new Dimension(445,595));
                revalidate();}}}
        
    class AddSuiteFrame extends JFrame{
        private static final long serialVersionUID = 1L;
        JButton ok ;
        JTextField namefield;
        JComboBox <String>epidfield;
        JComponent mainframe;
        
        public void okAction(Item suita,int pos){            
            FontMetrics metrics = getGraphics().getFontMetrics(new Font("TimesRoman", Font.BOLD, 14));                
            int width = metrics.stringWidth(namefield.getText());
            if(suita!=null){   
                if(pos==0){
                    for(int j = 0;j<suita.getSubItemsNr();j++){                        
                        suita.getSubItem(j).updatePos(suita.getPos().size(),new Integer(suita.getSubItem(j).getPos().get(suita.getPos().size()).intValue()+1));}
                    ArrayList <Integer> indexpos = (ArrayList <Integer>)suita.getPos().clone();
                    indexpos.add(new Integer(0));
                    Item item = new Item(namefield.getText(),2, -1,5, width+140,25 , indexpos);
                    item.setEpId(suita.getEpId());
                    suita.insertSubItem(item,0);
                    Repository.f.p.p1.sc.g.updateLocations(suita);
                    Repository.f.p.p1.sc.g.repaint();}
                else{ArrayList <Integer> indexpos = (ArrayList <Integer>)suita.getPos().clone();
                    indexpos.add(new Integer(pos));
                    Item item = new Item(namefield.getText(),2, -1,5, width+140,25 , indexpos);
                    item.setEpId(suita.getEpId());
                    suita.insertSubItem(item,pos);
                    Repository.f.p.p1.sc.g.updateLocations(suita);
                    Repository.f.p.p1.sc.g.repaint();}}
            else{ArrayList <Integer> indexpos = new ArrayList <Integer>();
                indexpos.add(new Integer(Repository.getSuiteNr()));
                Item item = new Item(namefield.getText(),2, -1, 5, width+140,25 , indexpos);
                item.setEpId(epidfield.getSelectedItem().toString());
                Repository.addSuita(item);
                Repository.f.p.p1.sc.g.updateLocations(Repository.getSuita(0));
                Repository.f.p.p1.sc.g.repaint();}
            //mainframe.setEnabled(true);
            //Repository.f.setEnabled(true);
            Repository.f.p.p1.sc.g.setCanRequestFocus(true);
            (SwingUtilities.getWindowAncestor(ok)).dispose();
            Repository.f.p.p1.sc.g.repaint();}
        
        public AddSuiteFrame(final JComponent mainframe,final Item suita,final int pos){
            //this.mainframe = mainframe;
            addWindowFocusListener(new WindowFocusListener(){
                public void windowLostFocus(WindowEvent ev){
                    toFront();}
                    public void windowGainedFocus(WindowEvent ev){}});
            //mainframe.setEnabled(false);
            setLayout(null);
            setResizable(false);
            setBounds(400,300,200,110);   
            JLabel name = new JLabel("Suite Name:");
            name.setBounds(5,5,80,20);
            name.setFont(new Font("TimesRoman", Font.PLAIN, 14));
            JLabel EPId = new JLabel("EpId:");
            EPId.setBounds(5,30,80,20);
            EPId.setFont(new Font("TimesRoman", Font.PLAIN, 14));
            namefield = new JTextField(30);
            namefield.setBounds(90,5,100,20);        
            File f = new File(Repository.temp+System.getProperty("file.separator")+"Twister"+System.getProperty("file.separator")+"EpID.txt");
            String line = null;                             
            InputStream in = null;
            try{String dir = Repository.getRemoteEpIdDir();
                String [] path = dir.split("/");
                StringBuffer result = new StringBuffer();
                if (path.length > 0) {
                    for (int i=0; i<path.length-1; i++){
                        result.append(path[i]);
                        result.append("/");}}
                System.out.println("EP: "+Repository.getRemoteEpIdDir());
                Repository.c.cd(result.toString());
                in = Repository.c.get(path[path.length-1]);}
            catch(Exception e){e.printStackTrace();};
            InputStreamReader inputStreamReader = new InputStreamReader(in);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);  
            StringBuffer b=new StringBuffer("");
            try{while ((line=bufferedReader.readLine())!= null){b.append(line+";");}
                bufferedReader.close();
                inputStreamReader.close();
                in.close();}
            catch(Exception e){e.printStackTrace();}        
            String  [] vecresult = b.toString().split(";");
            epidfield = new JComboBox<String>(vecresult);
            epidfield.setBounds(90,30,100,20);
            add(name);
            add(namefield);
            add(EPId);
            add(epidfield);   
            Repository.f.p.p1.sc.g.setCanRequestFocus(false);
            setVisible(true);
            ok = new JButton("OK");
            ok.setBounds(130,55,60,20);
            ok.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent ev){
                    okAction(suita,pos);}});
            addWindowListener(new WindowAdapter(){
                public void windowClosing(WindowEvent e){
                    //mainframe.setEnabled(true);
                    Repository.f.p.p1.sc.g.setCanRequestFocus(true);
                    (SwingUtilities.getWindowAncestor(ok)).dispose();}});
            Action actionListener = new AbstractAction(){
                public void actionPerformed(ActionEvent actionEvent){
                    JButton source = (JButton) actionEvent.getSource();
                    okAction(suita,pos);}};                    
            InputMap keyMap = new ComponentInputMap(ok);
            keyMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, 0), "action");            
            ActionMap actionMap = new ActionMapUIResource();
            actionMap.put("action", actionListener);            
            SwingUtilities.replaceUIActionMap(ok, actionMap);
            SwingUtilities.replaceUIInputMap(ok, JComponent.WHEN_IN_FOCUSED_WINDOW, keyMap);            
            add(ok);}}}
            
class CompareItems implements Comparator{   
    public int compare(Object emp1, Object emp2){ 
        return ((Item)emp1).getName().compareToIgnoreCase(((Item)emp2).getName());}}            
            
class XMLFilter extends FileFilter {//se ocupa de reprezentarea xml-ului in cazul ferestrei de alegere a xml-ului reprezentat
    public boolean accept(File f) {
        return f.isDirectory() || f.getName().toLowerCase().endsWith(".xml");}    
    public String getDescription() {return ".xml files";}}