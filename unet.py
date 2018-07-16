def unet_other(weights=None, input_size=(512, 512, 4)):
    inputs = Input(input_size)
    conv1 = Conv2D(32, 3, activation='elu', padding='same', kernel_initializer='he_normal')(inputs)
    conv1 = BatchNormalization()(conv1)
    conv1 = Conv2D(32, 3, activation='elu', padding='same', kernel_initializer='he_normal')(conv1)
    conv1 = BatchNormalization()(conv1)

    pool2 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(64, 3, activation='elu', padding='same', kernel_initializer='he_normal')(pool2)
    conv2 = BatchNormalization()(conv2)
    conv2 = Conv2D(64, 3, activation='elu', padding='same', kernel_initializer='he_normal')(conv2)
    conv2 = BatchNormalization()(conv2)

    pool3 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(128, 3, activation='elu', padding='same', kernel_initializer='he_normal')(pool3)
    conv3 = BatchNormalization()(conv3)
    conv3 = Conv2D(128, 3, activation='elu', padding='same', kernel_initializer='he_normal')(conv3)
    conv3 = BatchNormalization()(conv3)

    pool4 = MaxPooling2D(pool_size=(2, 2))(conv3)
    conv4 = Conv2D(256, 3, activation='elu', padding='same', kernel_initializer='he_normal')(pool4)
    conv4 = BatchNormalization()(conv4)
    conv4 = Conv2D(256, 3, activation='elu', padding='same', kernel_initializer='he_normal')(conv4)
    conv4 = BatchNormalization()(conv4)
    up4 = UpSampling2D(size=(2,2))(conv4)

    merge5  =concatenate([up4, conv3], axis=-1)
    drop5 = Dropout(0.5)(merge5)
    conv5 = Conv2D(128, 3, activation='elu', padding='same', kernel_initializer='he_normal')(drop5)
    conv5 = Conv2D(128, 3, activation='elu', padding='same', kernel_initializer='he_normal')(conv5)
    up5 = UpSampling2D(size=(2,2))(conv5)

    merge6 = concatenate([up5, conv2], axis=-1)
    drop6 = Dropout(0.5)(merge6)
    conv6 = Conv2D(64, 3,activation='elu', padding='same', kernel_initializer='he_normal')(drop6)
    conv6 = Conv2D(64, 3, activation='elu', padding='same', kernel_initializer='he_normal')(conv6)
    up6 = UpSampling2D(size=(2,2))(conv6)

    merge7 = concatenate([up6, conv1], axis=-1)
    drop7 = Dropout(0.5)(merge7)
    conv7 = Conv2D(32, 3, activation='elu',padding='same', kernel_initializer='he_normal')(drop7)
    conv7 = Conv2D(32, 3, activation='elu', padding='same', kernel_initializer='he_normal')(conv7)
    conv7 = Conv2D(1, 1, activation='sigmoid', padding='same', kernel_initializer='he_normal')(conv7)

    model = Model(input=inputs, output=conv7)

    model.compile(optimizer=Adam(lr=1e-4), loss=jaccard_coef_loss, metrics=['binary_crossentropy', jaccard_coef_int])

    with open('model-summary-report.txt', 'w') as fh:
        # Pass the file handle in as a lambda function to make it callable
        model.summary(print_fn=lambda x: fh.write(x + '\n'))

    if (weights):
        model.load_weights(weights)
    plot_model(model, to_file='unet-model.png',show_shapes=True)  #vis model
    return model
