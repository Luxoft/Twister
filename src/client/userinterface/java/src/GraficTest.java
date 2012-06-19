import java.awt.Canvas;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.Rectangle;
import java.awt.Font;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.PrintStream;
import javax.imageio.ImageIO;
import javax.swing.JPanel;
import java.awt.Dimension;
import java.util.ArrayList;
import java.util.Collections;

public class GraficTest extends JPanel{
    private static final long serialVersionUID = 1L;
    private boolean applet;
    private ArrayList <Integer> selected;
    private boolean foundfirstitem;
    private int y = 5;

    public GraficTest(int x, int y, boolean applet){
        this.applet = applet;
        setSize(445, 595);
        setBackground(new Color(190, 195, 195));
        addMouseListener(new MouseAdapter(){
            public void mouseReleased(MouseEvent ev){handleClick(ev);}});}
    
    /*
     * interpret mouse click
     */
    public void handleClick(MouseEvent ev){
        if(ev.getButton()==1){
            if(Repository.getTestSuiteNr()==0)return;
                getClickedItem(ev.getX(),ev.getY());
                if(selected.size()>0&&getItem(selected).getType()==2){
                    if(getItem(selected).getSubItemsNr()>0){getItem(selected).setVisible(!(getItem(selected).getSubItem(0).isVisible()));}
                    updateLocations(getItem(selected));}
                repaint();}}
    
    /*
     * get item based on ArrayList indices
     */
    public Item getItem(ArrayList <Integer> pos){           
        Item theone1 = Repository.getTestSuita(pos.get(0));
        for(int j=1;j<pos.size();j++){
            theone1 = theone1.getSubItem(pos.get(j));}
        return theone1;}
    
    /*
     * return item on location x,y
     */
    public void getClickedItem(int x, int y){
        Rectangle r = new Rectangle(x-1,y-1,2,2);
        int suitenr = Repository.getTestSuiteNr();
        selected = new ArrayList<Integer>();
        for(int i=0;i<suitenr;i++){
            if(handleClicked(r,Repository.getTestSuita(i))){
                selected.add(i);
                break;}}
        if(selected.size()>0)Collections.reverse(selected);}
     
    /*
     * handle click on specific item
     */
    public boolean handleClicked(Rectangle r, Item item){
        if(r.intersects(item.getRectangle())&&item.isVisible())return true;
        else{int itemnr = item.getSubItemsNr();
            for(int i=0;i<itemnr;i++){
                if(handleClicked(r,item.getSubItem(i))){
                    selected.add(i);
                    return true;}}
            return false;}}
     
    /*
     * update items location in tree view
     * starting from suita
     */
    public void updateLocations(Item suita){
        ArrayList <Integer> selected2 = (ArrayList <Integer>)suita.getPos().clone();
        if(selected2.size()>1){
            int index = selected2.get(0);
            selected2.remove(0);
            for(int i=index;i<Repository.getTestSuiteNr();i++){   
                Repository.window.mainpanel.p2.sc.g.iterateThrough(Repository.getTestSuita(i),selected2);
                selected2 = null;}}
        else if(selected2.size()==1){
            for(int i=selected2.get(0);i<Repository.getTestSuiteNr();i++){
                Repository.window.mainpanel.p2.sc.g.iterateThrough(Repository.getTestSuita(i),null);}}
        y=10;
        foundfirstitem=false;
        updateScroll();}
        
    /*
     * calculates previous position
     * for aligning on x
     */
    public int calcPreviousPositions(Item item){
        /*
         * calc diferently based on item type
         */
        ArrayList <Integer> pos = (ArrayList <Integer>)item.getPos().clone();
        if(item.getType()!=0){//it is not a prop
            if(pos.size()>1){
                pos.remove(pos.size()-1);
                Item temp = getItem(pos);
                return temp.getLocation()[0]+(int)(temp.getRectangle().getWidth()/2+20);}
            else{return 5;}}
        else{// it is prop should put beside it
            pos.remove(pos.size()-1);
            Item temp = getItem(pos);
            return temp.getLocation()[0]+(int)(temp.getRectangle().getWidth()+20);}}
        
    /*
     * positions the item based on
     * previous location
     */    
    public void positionItem(Item item){    
        if(item.getType()!=0){
            int x = calcPreviousPositions(item);
            item.setLocation(new int[]{x,y});
            y+=(int)(5+item.getRectangle().getHeight());}
        else{
            int x = calcPreviousPositions(item);
            item.setLocation(new int[]{x,(int)(y-5-item.getRectangle().getHeight())});}}
    
    /*
     * iterate through subitem of an item
     * and position it
     */
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
                
    /*
     * update scroll to adjust based
     * on view dimension
     */
    public void updateScroll(){
        int y1=0;
        for(int i=0;i<Repository.getTestSuiteNr();i++){
            if(Repository.getTestSuita(i).isVisible())y1 = getLastY(Repository.getTestSuita(i),y1);}
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
          
                
    /*
     * return last y position for last visible item
     */
    public int getLastY(Item item, int height){
        if(height<=(item.getRectangle().getY()+item.getRectangle().getHeight())){
            height=(int)(item.getRectangle().getY()+item.getRectangle().getHeight());        
            int nr = item.getSubItemsNr()-1;
            for(int i=nr;i>=0;i--){
                if(item.getSubItem(i).isVisible()){height = getLastY(item.getSubItem(i),height);}}
            return height;}
        else return height;}

    public void paint(Graphics g){
        g.setColor(Color.WHITE);
        g.fillRect(0,0,getWidth(),getHeight());
        g.setColor(Color.BLACK);
        int suitenr = Repository.getTestSuiteNr();
        for(int i=0;i<suitenr;i++){
            handlePaintItem(Repository.getTestSuita(i),g);}}
            
    public void handlePaintItem(Item item, Graphics g){
        drawItem(item,g);
        int subitemnr = item.getSubItemsNr();
        if(subitemnr>0&&item.getSubItem(0).isVisible()){
            for(int i=0;i<subitemnr;i++){handlePaintItem(item.getSubItem(i),g);}}}
             
            
    /*
     * handle drawing item based on
     * item type and it's properties
     */
    public void drawItem(Item item,Graphics g){
        g.setColor(Color.BLACK);
        g.setFont(new Font("TimesRoman", Font.PLAIN, 12));
        if(item.getType()==2){
            g.drawString(item.getName(),(int)item.getRectangle().getX()+25,(int)item.getRectangle().getY()+18);
            g.drawImage(Repository.getSuitaIcon(),(int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);}
        else if(item.getType()==1){
            if(!item.isRunnable())g.setColor(Color.GRAY);
            g.drawString(item.getName(),(int)item.getRectangle().getX()+30,(int)item.getRectangle().getY()+15);
            g.setColor(Color.BLACK);
            String value = item.getSubItem(0).getValue().toUpperCase();
            if(value.equals("FAIL")) g.drawImage(Repository.getFailIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("PENDING")) g.drawImage(Repository.getPendingIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("RUNNING")) g.drawImage(Repository.getWorkingIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("SKIPPED")) g.drawImage(Repository.getSkippedIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("STOPPED")) g.drawImage(Repository.getStoppedIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("NOT EXECUTED")) g.drawImage(Repository.getNotExecIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("TIMEOUT")) g.drawImage(Repository.getTimeoutIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("WAITING")) g.drawImage(Repository.getWaitingIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else if(value.equals("PASS")) g.drawImage(Repository.getPassIcon(), (int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);
            else g.drawImage(Repository.getTCIcon(),(int)item.getRectangle().getX()+5,(int)item.getRectangle().getY()+1,null);}
        else{
            g.drawImage(Repository.getPropertyIcon(),(int)item.getRectangle().getX()+2,(int)item.getRectangle().getY()+1,null);
            g.drawString(item.getName()+" : "+item.getValue(),(int)item.getRectangle().getX()+25,(int)item.getRectangle().getY()+15);}
        if((item.getPos().size()!=1)){
            if(item.getType()==0){}
            else{
                g.drawLine((int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),(int)item.getRectangle().getX(),(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2));
                ArrayList<Integer> temp = (ArrayList<Integer>)item.getPos().clone();
                if(temp.get(temp.size()-1)==0)g.drawLine((int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),(int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY())-5);
                else{
                    temp.set(temp.size()-1,new Integer(temp.get(temp.size()-1).intValue()-1));
                    Item theone = getItem(temp);
                    g.drawLine((int)item.getRectangle().getX()-25,(int)(item.getRectangle().getY()+item.getRectangle().getHeight()/2),(int)item.getRectangle().getX()-25,(int)(theone.getRectangle().getY()+theone.getRectangle().getHeight()/2));}}}
        if(item.getEpId()!=null){
            g.setFont(new Font("TimesRoman", Font.PLAIN, 11));
            g.drawString(" - "+item.getEpId(),(int)(item.getRectangle().getX()+item.getRectangle().getWidth()-20),(int)(item.getRectangle().getY()+18));}}}