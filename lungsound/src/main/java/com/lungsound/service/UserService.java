package com.lungsound.service;

import com.lungsound.model.Role;
import com.lungsound.model.User;

import java.util.List;

public interface UserService {
    User registerUser(String username , String password , Role role);
    User findByName(String username);
    List<User> getAllUsers();
    User updateUserRole(Long id , Role role);
    void deleteUser(Long id);
}
