/*
File: PermissionValidator.java ; This file is part of Twister.
Version: 2.005

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import java.util.Arrays;

public class PermissionValidator{
    private static String [] permissions;
    private static boolean crete_project,change_project,delete_project,change_fwm_cfg,
                           change_globals,run_tests,edit_tc,change_db_cfg,change_email,
                           changes_ervices,view_reports,change_plugins,change_sut;
    
    public static void init(String permissions){
        try{String str[] = permissions.split(",");
            Arrays.sort(str);
            PermissionValidator.permissions = str;
        } catch (Exception e){
            e.printStackTrace();
        }
        change_plugins = getPermission("CHANGE_PLUGINS");
        view_reports = getPermission("VIEW_REPORTS");
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
        change_sut = getPermission("CHANGE_SUT");
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
    
    public static boolean canChangeSut(){
        return change_sut;
    }
    
    public static boolean canViewReports(){
        return view_reports;
    }
    
    public static boolean canChangePlugins(){
        return change_plugins;
    }
}