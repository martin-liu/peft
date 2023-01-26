# coding=utf-8
# Copyright 2023-present the HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import json
import enum
from dataclasses import dataclass, field, asdict
from typing import Optional, Union

from huggingface_hub import hf_hub_download

from .adapters_utils import CONFIG_NAME


class PeftType(str, enum.Enum):
    PROMPT_TUNING = "PROMPT_TUNING"
    P_TUNING = "P_TUNING"
    PREFIX_TUNING = "PREFIX_TUNING"
    LORA = "LORA"


class TaskType(str, enum.Enum):
    SEQ_CLS = "SEQ_CLS"
    SEQ_2_SEQ_LM = "SEQ_2_SEQ_LM"
    CAUSAL_LM = "CAUSAL_LM"
    TOKEN_CLS = "TOKEN_CLS"

@dataclass
class PeftConfigMixin(object):
    peft_type: Optional[PeftType] = field(default=None, metadata={"help": "The type of PEFT model."})

    @property
    def __dict__(self):
        return asdict(self)

    def to_dict(self):
        return self.__dict__

    def save_pretrained(self, save_directory):
        if os.path.isfile(save_directory):
            raise AssertionError(f"Provided path ({save_directory}) should be a directory, not a file")

        os.makedirs(save_directory, exist_ok=True)

        output_dict = self.__dict__
        output_path = os.path.join(save_directory, CONFIG_NAME)

        # save it
        with open(output_path, "w") as writer:
            writer.write(json.dumps(output_dict))    
    
    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs):
        if os.path.isfile(os.path.join(pretrained_model_name_or_path, CONFIG_NAME)):
            config_file = os.path.join(pretrained_model_name_or_path, CONFIG_NAME)
        else:
            try:
                config_file = hf_hub_download(pretrained_model_name_or_path, CONFIG_NAME)
            except:
                raise ValueError(f"Can't find config.json at '{pretrained_model_name_or_path}'")
        
        loaded_attributes = cls.from_json_file(config_file)
        config = cls(**kwargs)

        for key, value in loaded_attributes.items():
            if hasattr(config, key):
                setattr(config, key, value)

        return config
        
    @classmethod
    def from_json_file(cls, json_file, **kwargs):
        with open(json_file, 'r') as file:
            json_object = json.load(file)

        return json_object


class PeftConfig(PeftConfigMixin):
    """
    This is the base configuration class to store the configuration of a :class:`~peft.PeftModel`.

    Args:
        peft_type (Union[[`~peft.utils.config.PeftType`], `str`]): The type of Peft method to use.
        task_type (Union[[`~peft.utils.config.TaskType`], `str`]): The type of task to perform.
        inference_mode (`bool`, defaults to `False`): Whether to use the Peft model in inference mode.
    """
    peft_type: Union[str, PeftType] = field(default=None, metadata={"help": "Peft type"})
    task_type: Union[str, TaskType] = field(default=None, metadata={"help": "Task type"})
    inference_mode: bool = field(default=False, metadata={"help": "Whether to use inference mode"})


class PromptLearningConfig(PeftConfig):
    """
    This is the base configuration class to store the configuration of a Union[[`~peft.PrefixTuning`],
    [`~peft.PromptEncoder`], [`~peft.PromptTuning`]].

    Args:
        num_virtual_tokens (`int`): The number of virtual tokens to use.
        token_dim (`int`): The hidden embedding dimension of the base transformer model.
        num_transformer_submodules (`int`): The number of transformer submodules in the base transformer model.
        num_attention_heads (`int`): The number of attention heads in the base transformer model.
        num_layers (`int`): The number of layers in the base transformer model.
    """

    num_virtual_tokens: int = field(default=None, metadata={"help": "Number of virtual tokens"})
    token_dim: int = field(
        default=None, metadata={"help": "The hidden embedding dimension of the base transformer model"}
    )
    num_transformer_submodules: Optional[int] = field(default=1, metadata={"help": "Number of transformer submodules"})
    num_attention_heads: Optional[int] = field(default=None, metadata={"help": "Number of attention heads"})
    num_layers: Optional[int] = field(default=None, metadata={"help": "Number of transformer layers"})
