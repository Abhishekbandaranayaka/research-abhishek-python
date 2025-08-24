package com.lungsound.service;

import com.lungsound.model.AudioClip;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface AudioClipService {

    AudioClip uploadAndPredict(MultipartFile file , String username);
    List<AudioClip> getAllClips();
    AudioClip getClipById(Long id);
    void deleteClip(Long id);

}
