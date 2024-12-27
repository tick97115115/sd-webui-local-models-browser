from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

### Lora model Start
class TagFrequency(BaseModel):
    luxuriouswheelscostume: int

class DatasetDirs(BaseModel):
    n_repeats: int
    img_count: int

class BucketInfo(BaseModel):
    resolution: List[int]
    count: int

class Buckets(BaseModel):
    buckets: Dict[str, BucketInfo] | None = None
    mean_img_ar_error: float | None = Field(default=None, alias="mean_img_ar_error")

class Metadata(BaseModel):
    ss_sd_model_name: Optional[str] = None
    ss_resolution: Optional[str] = None
    ss_clip_skip: Optional[str] = None
    ss_num_train_images: Optional[str] = None
    ss_tag_frequency: Optional[Dict[str, Any]] = Field(alias="ss_tag_frequency", default=None)
    ss_mixed_precision: Optional[str] = None
    ss_gradient_accumulation_steps: Optional[str] = None
    ss_training_finished_at: Optional[str] = None
    modelspec_title: Optional[str] = Field(alias="modelspec.title", default=None)
    ss_flip_aug: Optional[str] = None
    ss_seed: Optional[str] = None
    modelspec_implementation: Optional[str] = Field(alias="modelspec.implementation", default=None)
    ss_network_dropout: Optional[str] = None
    ss_noise_offset: Optional[str] = None
    ss_reg_dataset_dirs: Optional[Dict[str, Union[Dict, str]]] = Field(alias="ss_reg_dataset_dirs", default=None)
    ss_bucket_info: Buckets | str | None = Field(default=None, alias="ss_bucket_info")
    ss_steps: Optional[str] = None
    ss_output_name: Optional[str] = None
    modelspec_architecture: Optional[str] = Field(alias="modelspec.architecture", default=None)
    ss_dataset_dirs: Optional[Dict[str, DatasetDirs]] = Field(alias="ss_dataset_dirs", default=None)
    ss_keep_tokens: Optional[str] = None
    ss_epoch: Optional[str] = None
    sshs_legacy_hash: Optional[str] = None
    ss_num_epochs: Optional[str] = None
    ss_cache_latents: Optional[str] = None
    ss_adaptive_noise_scale: Optional[str] = None
    modelspec_resolution: Optional[str] = Field(alias="modelspec.resolution", default=None)
    ss_lr_warmup_steps: Optional[str] = None
    ss_lowram: Optional[str] = None
    ss_network_dim: Optional[str] = None
    ss_network_alpha: Optional[str] = None
    modelspec_sai_model_spec: Optional[str] = Field(alias="modelspec.sai_model_spec", default=None)
    ss_zero_terminal_snr: Optional[str] = None
    modelspec_date: Optional[str] = Field(alias="modelspec.date", default=None)
    sshs_model_hash: Optional[str] = None
    ss_multires_noise_discount: Optional[str] = None
    ss_scale_weight_norms: Optional[str] = None
    ss_max_token_length: Optional[str] = None
    ss_bucket_no_upscale: Optional[str] = None
    ss_max_train_steps: Optional[str] = None
    ss_enable_bucket: Optional[str] = None
    ss_base_model_version: Optional[str] = None
    ss_text_encoder_lr: Optional[str] = None
    ss_face_crop_aug_range: Optional[str] = None
    ss_ip_noise_gamma: Optional[str] = None
    ss_debiased_estimation: Optional[str] = None
    ss_batch_size_per_device: Optional[str] = None
    ss_total_batch_size: Optional[str] = None
    ss_unet_lr: Optional[str] = None
    ss_num_reg_images: Optional[str] = None
    ss_network_module: Optional[str] = None
    modelspec_prediction_type: Optional[str] = Field(alias="modelspec.prediction_type", default=None)
    ss_v2: Optional[str] = None
    ss_sd_scripts_commit_hash: Optional[str] = None
    ss_optimizer: Optional[str] = None
    ss_prior_loss_weight: Optional[str] = None
    ss_shuffle_caption: Optional[str] = None
    ss_max_grad_norm: Optional[str] = None
    ss_min_snr_gamma: Optional[str] = None
    ss_lr_scheduler: Optional[str] = None
    ss_caption_dropout_rate: Optional[str] = None
    ss_color_aug: Optional[str] = None
    ss_learning_rate: Optional[str] = None
    ss_training_comment: Optional[str] = None
    ss_full_fp16: Optional[str] = None
    ss_num_batches_per_epoch: Optional[str] = None
    ss_gradient_checkpointing: Optional[str] = None
    ss_caption_dropout_every_n_epochs: Optional[str] = None
    ss_session_id: Optional[str] = None
    ss_caption_tag_dropout_rate: Optional[str] = None
    ss_sd_model_hash: Optional[str] = None
    ss_random_crop: Optional[str] = None
    ss_min_bucket_reso: Optional[str] = None
    ss_max_bucket_reso: Optional[str] = None
    ss_new_sd_model_hash: Optional[str] = None
    ss_training_started_at: Optional[str] = None
    ss_multires_noise_iterations: Optional[str] = None

class UserMetadata(BaseModel):
    activation_text: str | None = Field(default=None, alias="activation text")
    description: str | None = None
    sd_version: Optional[str] = Field(alias="sd version", default=None)
    model_id: int | None | str = Field(default=None, alias="modelId")
    sha256: str | None = None

class ResponseBody_Lora(BaseModel):
    name: str
    filename: str
    shorthash: str
    preview: Optional[str] = None
    description: Optional[str] = None
    search_terms: List[str] = Field(alias="search_terms")
    local_preview: str
    metadata: Optional[Metadata]
    user_metadata: UserMetadata
    prompt: str
    negative_prompt: str
    sd_version: Optional[str] = None
    sd_version_str: str
    ctime: float

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    body: ResponseBody_Lora
    message: Optional[str] = None

### Lora model End

class Response_Loras:
    Loras: list[ResponseBody_Lora]
    number: int