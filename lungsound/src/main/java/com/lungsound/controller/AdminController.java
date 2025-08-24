package com.lungsound.controller;

import com.lungsound.model.AudioClip;
import com.lungsound.model.Role;
import com.lungsound.model.User;
import com.lungsound.service.AudioClipService;
import com.lungsound.service.ModelManagementService;
import com.lungsound.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    @Autowired
    private UserService userService;

    @Autowired
    private AudioClipService audioClipService;

    @Autowired
    private ModelManagementService modelManagementService;

    @GetMapping("/users")
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(userService.getAllUsers());
    }

    @PutMapping("/users/{userId}/role")
    public ResponseEntity<User> updateUserRole(@PathVariable Long userId, @RequestParam String role) {
        return ResponseEntity.ok(userService.updateUserRole(userId, Role.valueOf(role.toUpperCase())));
    }

    @DeleteMapping("/users/{userId}")
    public ResponseEntity<String> deleteUser(@PathVariable Long userId) {
        userService.deleteUser(userId);
        return ResponseEntity.ok("User deleted");
    }

    @GetMapping("/clips")
    public ResponseEntity<List<AudioClip>> getAllClips() {
        return ResponseEntity.ok(audioClipService.getAllClips());
    }

    @DeleteMapping("/clips/{clipId}")
    public ResponseEntity<String> deleteClip(@PathVariable Long clipId) {
        audioClipService.deleteClip(clipId);
        return ResponseEntity.ok("Clip deleted");
    }

    @PostMapping("/model/retrain")
    public ResponseEntity<String> retrainModel() {
        modelManagementService.triggerModelRetrainning();
        return ResponseEntity.ok("Retraining triggered");
    }

    @GetMapping("/model/metrics")
    public ResponseEntity<String> getModelMetrics() {
        return ResponseEntity.ok(modelManagementService.getModelMetrics());
    }

}
