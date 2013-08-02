import java.util.Arrays;

public class PermissionValidtor{
    private static String []permissions;
    private static boolean crete_project,change_project,delete_project,change_fwm_cfg,
                    change_globals,run_tests,edit_tc,change_db_cfg,change_email,changes_ervices;
    
    public static void init(String permissions){
        String str[] = permissions.split(",");
        Arrays.sort(str);
        PermissionValidtor.permissions = str;
        crete_project = getPermission("CREATE_PROJECT");
        change_project = getPermission("CHANGE_PROJECT");
        delete_project = getPermission("DELETE_PROJECT");
        change_fwm_cfg = getPermission("CHANGE_FWM_CFG");
        change_globals = getPermission("CHANGE_GLOBALS");
        run_tests = getPermission("RUN_TESTS");
        edit_tc = getPermission("EDIT_TC");
        change_db_cfg = getPermission("CHANGE_DB_CFG");
        change_email = getPermission("CHANGE_EML_CFG");
        changes_ervices = getPermission("CHANGE_SERVICES");
        
    }
    
    private static boolean getPermission(String permission){
        try{
            if(Arrays.binarySearch(permissions, permission)>-1)return true;
            return false;
        } catch (Exception e){
            return false;
        }
    }
    
    public static boolean canCreateProject(){
        return crete_project;
    }
    
    public static boolean canChangeProject(){
        return change_project;
    }
    
    public static boolean canDeleteProject(){
        return delete_project;
    }
    
    public static boolean canChangeFWM(){
       return change_fwm_cfg;
    }
    
    public static boolean canChangeGlobals(){
        return change_globals;
    }
    
    public static boolean canRunTests(){
        return run_tests;
    }
    
    public static boolean canEditTC(){
        return edit_tc;
    }
    
    public static boolean canEditDB(){
        return change_db_cfg;
    }
    
    public static boolean canEditEmail(){
        return change_email;
    }
    
    public static boolean canEditServices(){
        return changes_ervices;
    }
}