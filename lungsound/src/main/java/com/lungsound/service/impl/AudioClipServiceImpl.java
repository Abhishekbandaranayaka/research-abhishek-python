package com.lungsound.service.impl;

import com.lungsound.model.AudioClip;
import com.lungsound.model.User;
import com.lungsound.repository.AudioClipRepository;
import com.lungsound.service.AudioClipService;
import com.lungsound.service.UserService;
import org.apache.coyote.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@Service
public class AudioClipServiceImpl implements AudioClipService {

    @Autowired
    private AudioClipRepository audioClipRepository;

    @Autowired
    private UserService userService;

    private RestTemplate restTemplate;

    private final String modelServiceUrl = "http://model-service:8001/predict";

    @Override
    public AudioClip uploadAndPredict(MultipartFile file, String username) {
        User user = userService.findByName(username);
        LinkedMultiValueMap<String , Object> map = new LinkedMultiValueMap<>();
        map.add("file" , file.getResource());
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<LinkedMultiValueMap<String , Object>> request = new HttpEntity<>(map , headers);
        ResponseEntity<String> response = restTemplate.postForEntity(modelServiceUrl , request, String.class);
        String prediction = response.getBody().replace("{\"prediction\":\"", "").replace("\"}", "");

        AudioClip clip = new AudioClip();
        clip.setUser(user);
        clip.setFileName(file.getOriginalFilename());
        clip.setPrediction(prediction);
        return audioClipRepository.save(clip);
    }

    @Override
    public List<AudioClip> getAllClips() {
        return audioClipRepository.findAll();
    }

    @Override
    public AudioClip getClipById(Long clipId) {
        return audioClipRepository.findById(clipId)
                .orElseThrow(() -> new RuntimeException("Clip not found"));
    }

    @Override
    public void deleteClip(Long id) {
        audioClipRepository.deleteById(id);
    }
}
