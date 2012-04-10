import java.awt.Rectangle;
import java.util.ArrayList;

public class Item implements Cloneable{
    private int type;
    private String name,value;//numele
    private boolean selected = false;// in cazul ca e selectata suita pentru reprezentare grafica
    private Rectangle rectangle=new Rectangle();// dreptunghiul aferent suitei sau tc-ului in cadrul reprezentarii grafice
    private Rectangle checkrectangle=new Rectangle(); // dreptunghiul aferent check-ului suitei sau tc-ului in cadrul reprezentarii grafice
    private boolean visible = true;//tine cont daca este vizibil el in cazul tc sau ce contine el
    private ArrayList <Item> subitems = new ArrayList<Item>();//contine tc-uri si/sau suite sau proprietati 
    private ArrayList <Integer> indexpos;
    private boolean check = true;
    private String EpID;    
    private boolean runnable = true;
    private ArrayList<String[]> userDefined = new ArrayList<String[]>();
    
    public Item(String name,int type, int x, int y, int width, int height, ArrayList <Integer> indexpos){
        this.indexpos = indexpos;
        this.type = type;
        this.name = name;
        rectangle.setLocation(x,y);
        rectangle.setSize(width,height);
        if(type!=0){
            checkrectangle.setLocation(x+3,y+3);
            checkrectangle.setSize(height-6,height-6);}}
    
    public void setName(String name){
        this.name = name;}
        
    public String getName(){
        return name;}
        
    protected Item clone(){
        try{Item clone = (Item)super.clone();
            clone.subitems = (ArrayList <Item>)subitems.clone();
            for(int i=0;i<clone.getSubItemsNr();i++){clone.subitems.set(i, clone.getSubItem(i).clone());}
            return clone;}
        catch(CloneNotSupportedException e){
            e.printStackTrace();
            return null;}}
        
    public void setSubItemVisible(boolean visible){
        this.visible = visible;
        int subitemsnr = subitems.size();
        for(int i=0;i<subitemsnr;i++) getSubItem(i).setSubItemVisible(visible);}
        
    public void setVisible(boolean visible){
        int subitemsnr = subitems.size();
        for(int i=0;i<subitemsnr;i++) getSubItem(i).setSubItemVisible(visible);}
        
    public void setVisibleTC(){
        if(subitems.size()>0&&getSubItem(0).getType()==0){
            setVisible(false);}
        else{
            setVisible(true);
            int subitemsnr = subitems.size();
            for(int i=0;i<subitemsnr;i++) getSubItem(i).setVisibleTC();}}
        
    public boolean isVisible(){
        return visible;}
        
    public int getSubItemsNr(){
        return subitems.size();}
       
    public Item getSubItem(int nr){
        return subitems.get(nr);}
        
    public void updatePos(int index,Integer newvalue){
        indexpos.set(index,newvalue);
        for(int i=0;i<subitems.size();i++){
            subitems.get(i).updatePos(index,newvalue);}}
        
    public ArrayList<Item> getSubItems(){
        return subitems;}
        
    public void addSubItem(Item s){
        subitems.add(s);}
        
    public void insertSubItem(Item s, int index){
        subitems.add(index,s);}
        
    public void select(boolean select){
        selected = select;}
        
    public void selectAll(Item item,boolean select){
        item.select(select);
        for(int i=0;i<item.getSubItemsNr();i++){selectAll(item.getSubItem(i),select);}}
        
    public boolean isSelected(){
        return selected;}
        
    public Rectangle getCheckRectangle(){
        return checkrectangle;}
        
    public Rectangle getRectangle(){
        return rectangle;}
        
    public void setRectangle(Rectangle rectangle){
        this.rectangle = rectangle;}
        
    public void setLocation(int [] pos){
        getRectangle().setLocation(pos[0],pos[1]);
        if(type!=0) checkrectangle.setLocation(pos[0]+3,pos[1]+3);}
        
    public int[] getLocation(){
        return (new int [] {(int)rectangle.getLocation().getX(),(int)rectangle.getLocation().getY()});}
        
    public String getEpId(){
        return EpID;}
        
    public void setEpId(String EpID){
        this.EpID = EpID;
        for(Item item:subitems){
            if(item.getType()==2)item.setEpId(EpID);}}
    
    public void setCheck(boolean check){
        this.check = check;
        if(type==2){
            int nr = subitems.size();
            for(int i=0;i<nr;i++){
                subitems.get(i).setCheck(check);}}
        else subitems.get(0).setValue(check+"");}
        
    public boolean getCheck(){
        return check;}
    
    public void setRunnable(boolean cond){
        runnable = cond;}  
        
    public void switchRunnable(){
        runnable = !runnable;}
        
    public boolean isRunnable(){
        return runnable;}
    
    public int getType(){
        return type;}
        
    public String getValue(){
        return value;}
        
    public String getFileLocation(){
        return name;}
        
    public void setValue(String value){
        this.value = value;}
        
    public void setPos(ArrayList<Integer> indexpos){
        this.indexpos=indexpos;
        for(int i=0;i<getSubItemsNr();i++){
            ArrayList<Integer> clona = (ArrayList<Integer>)indexpos.clone();
            clona.add(new Integer(i));
            getSubItem(i).setPos(clona);}}
            
    public boolean contains(Item item,Item test){
        if(test==null){
            if(this==item)return true;}
        else{
            if(test==item)return true;
            else{
                for(int i=0;i<getSubItemsNr();i++){
                    if(contains(item,getSubItem(i))){
                        return true;}}}}
        return false;}
        
    public void addUserDef(String [] userdef){
        userDefined.add(userdef);}
        
    public int getUserDefNr(){
        return userDefined.size();}
        
    public ArrayList<String[]>getUserDefs(){
        return userDefined;}
        
    public String [] getUserDef(int i){
        return userDefined.get(i);}
        
    public void setUserDef(int index,String description,String userDef){
        if(userDefined.size()-1<index){
            for(int i=userDefined.size();i<index+1;i++){
                userDefined.add(new String[]{"",""});}}
        String temp [] = userDefined.get(index);
        temp[0] = description;
        temp[1] = userDef;
        userDefined.set(index, temp);}
        
    public Item getFirstSuitaParent(boolean test){
        ArrayList <Integer> temp = (ArrayList <Integer>)indexpos.clone();
        if(temp.size()==1)return null;
        if(getType()==1||getType()==2){
            temp.remove(temp.size()-1);
            return Grafic.getItem(temp,test);}
        else{
            temp.remove(temp.size()-1);
            temp.remove(temp.size()-1);
            return Grafic.getItem(temp,test);}}
            
    public Item getTcParent(boolean test){
        ArrayList <Integer> temp = (ArrayList <Integer>)indexpos.clone();
        if(getType()==0){
            temp.remove(temp.size()-1);
            return Grafic.getItem(temp,test);}
        return null;}
            
    public Item getParent(boolean test){
        if(indexpos.size()>1){
            ArrayList <Integer> temp = new ArrayList <Integer>();
            temp.add(indexpos.get(0));
            return Grafic.getItem(temp,test);}
        else return null;}
    
    public ArrayList<Integer> getPos(){
        return indexpos;}}