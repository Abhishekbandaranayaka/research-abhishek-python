package com.lungsound.controller;

import com.lungsound.model.AudioClip;
import com.lungsound.service.AudioClipService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api")
public class PredictionController {

    @Autowired
    private AudioClipService audioClipService;

    @PostMapping("/predict")
    public ResponseEntity<AudioClip> predict(@RequestParam("file") MultipartFile file) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        AudioClip result = audioClipService.uploadAndPredict(file, username);
        return ResponseEntity.ok(result);
    }

}
