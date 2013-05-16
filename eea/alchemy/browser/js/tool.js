if(window.EEA === undefined){
  var EEA = {
    who: 'eea.alchemy',
    version: '5.0'
  };
}

EEA.AlchemyDiscoverer = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.AlchemyDiscoverer.prototype = {
  initialize: function(){
    var self = this;
    self.ctypes = jQuery('.alchemy-box:nth-child(1)', self.context);
    self.lookin = jQuery('.alchemy-box:nth-child(2)', self.context);
    self.lookfor = jQuery('.alchemy-box:nth-child(3)', self.context);
    self.buttons = jQuery('.alchemy-button', self.context);

    // Content-Type
    jQuery('input', self.ctypes).click(function(evt, item){
      var checked = jQuery(this).parents('.alchemy-box').find(':checked');
      if(checked.length){
        self.lookin.show();
      }else{
        self.lookfor.find(':checked').click();
        self.lookin.find(':checked').click();
        self.buttons.hide();
        self.lookfor.hide();
        self.lookin.hide();
      }
    });

    // Look in
    jQuery('input', self.lookin).bind('click', function(evt, item){
      var checked = jQuery(this).parents('.alchemy-box').find(':checked');
      if(checked.length){
        self.lookfor.show();
      }else{
        self.lookfor.find(':checked').click();
        self.buttons.hide();
        self.lookfor.hide();
      }
    });

    // Look for
    jQuery('input', self.lookfor).click(function(evt, item){
      var checked = jQuery(this).parents('.alchemy-box').find(':checked');
      if(checked.length){
        self.buttons.show();
      }else{
        self.buttons.hide();
      }
    });

    self.reload();
  },

  reload: function(){
    var self = this;
    jQuery('.alchemy-box', self.context).hide();
    self.ctypes.show();
  }
};

jQuery.fn.EEAlchemyDiscoverer = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.AlchemyDiscoverer(context, options);
    context.data('EEAlchemyDiscoverer', adapter);
  });
};

// On document ready
jQuery(document).ready(function(){
  // Cleanup main template
  jQuery("#belowContent").remove();
  jQuery("#eea-comments").remove();
  jQuery(".discussion").remove();

  // Initialize
  jQuery('#eea-alchemy .alchemy-search').EEAlchemyDiscoverer();
});
