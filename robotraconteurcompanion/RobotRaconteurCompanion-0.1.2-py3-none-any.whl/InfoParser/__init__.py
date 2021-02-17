import yaml
import RobotRaconteur as RR
from RobotRaconteur.RobotRaconteurPythonUtil import SplitQualifiedName
import traceback
import numpy as np
import uuid

def _find_by_name(v,name):
    for i in v:
        if (i.Name==name):
            return i
    return None

class InfoParser(object):
    def __init__(self, node = None, client_obj = None):
        if node is None:
            self.node = RR.RobotRaconteurNode.s
        else:
            self.node = node
        self.client_obj = client_obj

    def _find_namedarray(self, n):
        try:
            dtype = self.node.GetNamedArrayDType(n,self.client_obj)
        except:
            return None, None
        service_name, n1 = SplitQualifiedName(n)
        type_def = _find_by_name(self.node.GetServiceType(service_name).NamedArrays,n1)
        assert type_def is not None
        return dtype, type_def

    def _find_structure(self, s):
        try:
            stype = self.node.GetStructureType(s,self.client_obj)
        except:
            return None, None
        service_name, s1 = SplitQualifiedName(s)
        type_def = _find_by_name(self.node.GetServiceType(service_name).Structures,s1)
        assert type_def is not None
        return stype, type_def

    def _find_enum(self, s):
        service_name, s1 = SplitQualifiedName(s)
        try:
            return _find_by_name(self.node.GetServiceType(service_name).Enums,s1)
        except:
            return None
    
    def _rr_type_to_dtype(self,rr_type_code):
        if rr_type_code == RR.DataTypes_double_t:
            return np.float64
        if rr_type_code == RR.DataTypes_single_t:
            return np.float32
        if rr_type_code == RR.DataTypes_int8_t:
            return np.int8
        if rr_type_code == RR.DataTypes_uint8_t:
            return np.uint8
        if rr_type_code == RR.DataTypes_int16_t:
            return np.int16
        if rr_type_code == RR.DataTypes_uint16_t:
            return np.uint16
        if rr_type_code == RR.DataTypes_int32_t:
            return np.int32
        if rr_type_code == RR.DataTypes_uint32_t:
            return np.uint32
        if rr_type_code == RR.DataTypes_int64_t:
            return np.int64
        if rr_type_code == RR.DataTypes_uint64_t:
            return np.uint64        
    
    def _check_array_len(self,arr,type_def):
        if type_def.ArrayVarLength == True:
            if len(type_def.ArrayLength) == 0 or type_def.ArrayLength[0] == 0:
                return True
            if len(arr) <= type_def.ArrayLength[0]:
                return True
            return False
        else:
            return len(arr) == type_def.ArrayLength[0]

    def _parse_number(self,d,type_def):
        if type_def.ArrayType == RR.DataTypes_ArrayTypes_none:
            if type_def.Type == RR.DataTypes_double_t or type_def.Type == RR.DataTypes_single_t:
                return float(d)
            else:
                if isinstance(d,str):
                    return int(d,0)
                else:                    
                        return int(d)
        elif type_def.ArrayType == RR.DataTypes_ArrayTypes_array:
            f_dtype = self._rr_type_to_dtype(type_def.Type)
            arr = np.array(d,dtype=f_dtype)
            assert self._check_array_len(arr,type_def)
            return arr
        elif type_def.ArrayType == RR.DataTypes_ArrayTypes_multidimarray:
            # TODO: handle more than fixed 2D multidim arrays
            if len(type_def.ArrayLength) != 2:
                return None
            f_dtype = self._rr_type_to_dtype(type_def.Type)
            arr = np.array(d,dtype=f_dtype)
            return arr.reshape(type_def.ArrayLength,order="F")
        else:
            return None

    def _parse_structure(self, d, struct_type, struct_def):        
        service_def = struct_def.GetServiceDefinition()
        struct_type_name = service_def.Name + "." + struct_def.Name
        s_override = "_override_structure_" + struct_type_name.replace(".","__")
        if hasattr(self,s_override):
            ov_res,ov_val = getattr(self,s_override)(d,struct_type,struct_def)
            if ov_res:
                return ov_val
        ret = struct_type()
        for i in range(len(struct_def.Members)):
            f_def = struct_def.Members[i]
            f_name = f_def.Name
            if not f_name in d:
                continue
            f_override = "_override_field_" + (service_def.Name + "." + struct_def.Name + "." + f_def.Name).replace(".","__")
            if hasattr(self,f_override):
               f_res = getattr(self,f_override)(d[f_name],f_def.Type,service_def)
               setattr(ret,f_name,f_res)
               continue
            f_res,f_val = self._parse_field_value(d[f_name], f_def.Type, struct_def, service_def)
            if f_res:
                setattr(ret,f_name,f_val)
                continue

        return ret
        
    def _parse_field_value(self, d, f_type, struct_def, service_def):
        
        if f_type.ContainerType != RR.DataTypes_ContainerTypes_none:
            f_type_e = f_type.Clone()
            f_type_e.RemoveContainers()
            if f_type.ContainerType == RR.DataTypes_ContainerTypes_list:
                ret = []
                for e in d:
                    e_res,e_val = self._parse_field_value(e,f_type_e,struct_def,service_def)
                    assert e_res
                    ret.append(e_val)
                return True,ret
            if f_type.ContainerType == RR.DataTypes_ContainerTypes_map_int32:
                ret = {}
                for k,v in d:
                    e_res,e_val = self._parse_field_value(e,f_type_e,struct_def,service_def)
                    assert e_res
                    ret[int(k,0)] = e_val
                return True,ret
            if f_type.ContainerType == RR.DataTypes_ContainerTypes_map_string:
                ret = {}
                for k,v in d:
                    e_res,e_val = self._parse_field_value(e,f_type_e,struct_def,service_def)
                    assert e_res
                    ret[str(k)] = e_val
                return True,ret
        if RR.IsTypeNumeric(f_type.Type):
            f_res = self._parse_number(d,f_type)
            if f_res is not None:
                return True, f_res
        
        if f_type.Type == RR.DataTypes_string_t:
            return True,str(d)
            
        
        if f_type.Type == RR.DataTypes_namedtype_t:
            typename = f_type.TypeString
            if "." not in typename:
                typename = service_def.Name + "." + typename            
            s_type, s_def = self._find_structure(typename)
            if s_type is not None:
                return True, self._parse_structure(d,s_type,s_def)
            n_dtype, n_def = self._find_namedarray(typename)
            if n_dtype is not None:
                return True, self._parse_namedarray(d,f_type,n_dtype,n_def)
            e_def = self._find_enum(typename)
            if e_def is not None:
                enum_val = _find_by_name(e_def.Values,str(d))
                assert enum_val is not None, "Invalid enum value"
                return True, int(enum_val.Value)           
        return False,None        

    def _parse_namedarray_el(self, d, arr, ind, d_type):
        
        for k,v in d_type.fields.items():
            if v[0].fields is not None:
                self._parse_namedarray_el(d[k],arr[ind],k,v[0])
            else:
                arr[ind][k] = np.array(d[k],dtype=v[0])   

    def _parse_namedarray(self, d, f_type, namedarray_dtype, namedarray_def):
        service_def = namedarray_def.GetServiceDefinition()
        namedarray_type_name = service_def.Name + "." + namedarray_def.Name
        n_override = "_override_namedarray_" + namedarray_type_name.replace(".","__")
        if hasattr(self,n_override):
            return getattr(self,n_override)(d,f_type,namedarray_dtype,namedarray_def)
        if f_type.ArrayType == RR.DataTypes_ArrayTypes_none:
            arr = np.zeros((1,),dtype=namedarray_dtype)
            self._parse_namedarray_el(d,arr,0,namedarray_dtype)
            return arr
        return None

    def ParseInfoFile(self, filename, type_name):
        struct_type = self._find_structure(type_name)

        with open(filename, 'r') as f:
            file_text = f.read()

        return ParseInfoString(self, file_text, type_name)

    def ParseInfoString(self, info_string, type_name):
        struct_type, struct_def = self._find_structure(type_name)
        if struct_type is None:
            raise RR.InvalidArgumentException("Invalid structure type specified")
        
        d = yaml.safe_load(info_string)
        
        ret = self._parse_structure(d,struct_type,struct_def)
        return ret

    ## Overrides for standard types

    def _override_field_com__robotraconteur__robotics__robot__RobotInfo__robot_capabilities(self, d, f_type, service_def):
        enum_def = _find_by_name(service_def.Enums,"RobotCapabilities")
        return self._flags_override(d,enum_def)
    
    def _override_field_com__robotraconteur__robotics__tool__ToolInfo__tool_capabilities(self, d, f_type, service_def):
        enum_def = _find_by_name(service_def.Enums,"ToolCapabilities")
        return self._flags_override(d,enum_def)

    def _override_field_com__robotraconteur__servo__ServoInfo__capabilities(self, d, f_type, service_def):
        enum_def = _find_by_name(service_def.Enums,"ServoCapabilities")
        return self._flags_override(d,enum_def)

    def _flags_override(self, d, enum_def):
        ret = 0
        for e in d:
            enum_val = _find_by_name(enum_def.Values,e)
            assert enum_val is not None, "Invalid flag name"
            ret |= int(enum_val.Value)
        return ret

    def _override_namedarray_com__robotraconteur__uuid__UUID(self,d,f_type,namedarray_dtype,namedarray_def):
        ret_uuid = uuid.UUID(str(d))
        ret_bytes = np.frombuffer(ret_uuid.bytes,dtype=np.uint8)
        ret = np.zeros((1,),dtype=namedarray_dtype)
        ret[0]["uuid_bytes"]=ret_bytes
        return ret

    def _override_structure_com__robotraconteur__identifier__Identifier(self, d, struct_type, struct_def):        
        if isinstance(d,str) or isinstance(d,int) or isinstance(d,float):
            ret = struct_type()
            ret.name = str(d)
            return True,ret
        return False,None

    def _override_field_com__robotraconteur__imaging__camerainfo__CameraCalibration__distortion_info(self,d,f_type,service_def):
        s_type,s_def = self._find_structure('com.robotraconteur.imaging.camerainfo.PlumbBobDistortionInfo')
        assert s_type is not None
        return RR.VarValue(self._parse_structure(d,s_type,s_def),'com.robotraconteur.imaging.camerainfo.PlumbBobDistortionInfo')
        