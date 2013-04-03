public class Path{
    private String path;
    
    public Path(String path)
    {
        this.path = path;
    }
    
    public String getPath(){
        return path;
    }
    
    public void setPath(String path){
        this.path = path;
    }
    
    public String toString(){
        return "Path: "+path;
    }
}
