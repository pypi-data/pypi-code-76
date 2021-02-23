import pytest
from typing import Callable
from tensorflow.keras.applications import DenseNet121, EfficientNetB0, InceptionV3, InceptionResNetV2, \
    MobileNetV3Small, NASNetMobile, ResNet50V2, VGG16, Xception

from test.utils import convert_and_assert


@pytest.mark.slow
@pytest.mark.parametrize('data_format', ["channels_last", "channels_first"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_densenet(data_format: str, test_infer: bool):
    convert_and_assert(DenseNet121, data_format, test_infer)

# Removing data_format = channels_first because of a bug in tensorflow (2.4) not able to generate EfficientNetB0 in
# that format
@pytest.mark.slow
@pytest.mark.parametrize('data_format', ["channels_last"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_efficientnet(data_format: str, test_infer: bool):
    convert_and_assert(EfficientNetB0, data_format, test_infer)


@pytest.mark.slow
@pytest.mark.parametrize('model', [InceptionV3, InceptionResNetV2])
@pytest.mark.parametrize('data_format', ["channels_last", "channels_first"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_inception(model: Callable, data_format: str, test_infer: bool):
    convert_and_assert(model, data_format, test_infer)


@pytest.mark.skip("fix issue with TFopLambda layer before running")
@pytest.mark.slow
@pytest.mark.parametrize('data_format', ["channels_last", "channels_first"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_mobilenet(data_format: str, test_infer: bool):
    convert_and_assert(MobileNetV3Small, data_format, test_infer)


# NASNetMobile have a problem with creating a channels_first model
@pytest.mark.slow
@pytest.mark.parametrize('data_format', ["channels_last"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_nasnet(data_format: str, test_infer: bool):
    convert_and_assert(NASNetMobile, data_format, test_infer)


@pytest.mark.slow
@pytest.mark.parametrize('data_format', ["channels_last", "channels_first"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_resnet(data_format: str, test_infer: bool):
    convert_and_assert(ResNet50V2, data_format, test_infer)


@pytest.mark.slow
@pytest.mark.parametrize('data_format', ["channels_last", "channels_first"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_vgg(data_format: str, test_infer: bool):
    convert_and_assert(VGG16, data_format, test_infer)


@pytest.mark.slow
@pytest.mark.parametrize('data_format', ["channels_last", "channels_first"])
@pytest.mark.parametrize("test_infer", [True, False])
def test_xception(data_format: str, test_infer: bool):
    convert_and_assert(Xception, data_format, test_infer)
