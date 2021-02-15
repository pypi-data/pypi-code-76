depends = ('ITKPyBase', 'ITKImageSources', 'ITKImageFilterBase', 'ITKCommon', )
templates = (
  ('ProxTVImageFilter', 'itk::ProxTVImageFilter', 'itkProxTVImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('ProxTVImageFilter', 'itk::ProxTVImageFilter', 'itkProxTVImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('ProxTVImageFilter', 'itk::ProxTVImageFilter', 'itkProxTVImageFilterIF4IF4', True, 'itk::Image< float,4 >, itk::Image< float,4 >'),
  ('ProxTVImageFilter', 'itk::ProxTVImageFilter', 'itkProxTVImageFilterID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('ProxTVImageFilter', 'itk::ProxTVImageFilter', 'itkProxTVImageFilterID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('ProxTVImageFilter', 'itk::ProxTVImageFilter', 'itkProxTVImageFilterID4ID4', True, 'itk::Image< double,4 >, itk::Image< double,4 >'),
)
