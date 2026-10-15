jQuery(document).ready(function($) {
    $('.member-modal-button').on('click', function(){
        var memberModal = $('#member-modal');
        var memberModalHeader = memberModal.find('.modal-header');
        var memberModalContent = memberModal.find('.modal-content');
        memberModalHeader.html("");
        $.ajax({
            url: hep.site_url + "/wp-json/hi-api/member/get-modal/"+$(this).data('id'),
            dataType: 'json',
            success: function (modal, textStatus, xhr) {
                memberModalHeader.html(modal.header);
                memberModalContent.html(modal.content);
                memberModalContent.foundation();
                memberModal.foundation('open');
            }
        });
    });

    var profilePhotoUpdater = $('#change-profile-photo-form');
    if(profilePhotoUpdater.length){
        profilePhotoUpdater.on('submit', function(e){
            e.preventDefault();

            const fd = new FormData();

            const profile_photo = $(this).find('#profile_photo');
            const file = profile_photo[0].files[0];
            const formNotice = profilePhotoUpdater.find('.form-notice');

            fd.append( "profile_photo", file);
            fd.append( "_wpnonce", member_ajax.nonce);
            
            jQuery.ajax({
                url: hep.site_url + "/wp-json/hi-api/member/change-avatar",
                type: 'POST',
                data: fd, 
                processData: false,
                contentType: false,

                success: function (response, textStatus, xhr) {
                    if(response.status != 'OK'){
                        formNotice.html(response.message);
                    } else {
                        var avatar = $('.member-avatar-container .hic-image');
                        formNotice.html(response.message);
                        avatar.css('background-image', 'url('+response.data.url+')')
                    }
                }
            });
        });
    }
});