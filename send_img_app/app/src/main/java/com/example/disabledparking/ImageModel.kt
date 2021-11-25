package com.example.disabledparking

data class ImageModel(
    val url: String,
    val location: String
) {
    constructor(): this("", "")
}
